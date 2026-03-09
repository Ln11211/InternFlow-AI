from openai import OpenAI
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import json

# NVIDIA Nemotron via OpenAI-compatible API
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# ── State shared across all agent nodes ──────────────────────────────────────
class AgentState(TypedDict):
    job_description: str
    resume_text: str
    projects: List[dict]       # List of all user projects
    keywords_missing: List[str]
    selected_projects: List[dict]
    tailored_resume: str
    diagnostic_report: str

# ── Node 1: Extract keywords from JD and find gaps ───────────────────────────
def keyword_diagnostic_node(state: AgentState) -> AgentState:
    prompt = f"""You are an expert ATS resume analyzer.

Given this Job Description:
{state['job_description']}

And this Resume:
{state['resume_text']}

Your task:
1. Extract the top 15 required keywords/skills from the JD
2. Identify which ones are MISSING from the resume
3. Return ONLY a JSON object in this exact format:
{{
  "jd_keywords": ["keyword1", "keyword2", ...],
  "missing_keywords": ["missing1", "missing2", ...],
  "present_keywords": ["present1", "present2", ...],
  "match_score": 75
}}"""

    response = client.chat.completions.create(
        model="nvidia/llama-3.3-nemotron-super-49b-v1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=800
    )

    raw = response.choices[0].message.content.strip()

    # Parse JSON safely
    try:
        # Extract JSON from response
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])
        state["keywords_missing"] = data.get("missing_keywords", [])
        state["diagnostic_report"] = json.dumps(data, indent=2)
    except Exception:
        state["keywords_missing"] = []
        state["diagnostic_report"] = raw

    return state

# ── Node 2: Select best projects for this specific JD ────────────────────────
def project_selector_node(state: AgentState) -> AgentState:
    if not state.get("projects"):
        state["selected_projects"] = []
        return state

    projects_text = "\n".join([
        f"- {p['name']}: {p['description']}" 
        for p in state["projects"]
    ])

    prompt = f"""You are an expert technical recruiter helping a student pick the best projects for a job application.

Job Description:
{state['job_description']}

Student's Available Projects:
{projects_text}

Task: Select the TOP 3 most relevant projects for this specific role.
Return ONLY a JSON array with the project names:
["Project Name 1", "Project Name 2", "Project Name 3"]

Think about: required skills, domain match, impact relevance."""

    response = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-nano-8b-v1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=200
    )

    raw = response.choices[0].message.content.strip()

    try:
        start = raw.find("[")
        end = raw.rfind("]") + 1
        selected_names = json.loads(raw[start:end])
        state["selected_projects"] = [
            p for p in state["projects"] 
            if p["name"] in selected_names
        ]
    except Exception:
        state["selected_projects"] = state["projects"][:3]

    return state

# ── Node 3: Rewrite resume tailored to the JD ────────────────────────────────
def resume_modifier_node(state: AgentState) -> AgentState:
    selected_projects_text = "\n".join([
        f"- {p['name']}: {p['description']}"
        for p in state.get("selected_projects", [])
    ]) or "Use projects already in the resume."

    missing_keywords = ", ".join(state.get("keywords_missing", [])) or "None"

    prompt = f"""You are an expert resume writer. Rewrite the resume below to be perfectly tailored for this job.

Job Description:
{state['job_description']}

Original Resume:
{state['resume_text']}

Selected Projects to highlight:
{selected_projects_text}

Missing keywords to naturally incorporate:
{missing_keywords}

Instructions:
- Keep the same structure and format
- Naturally weave in missing keywords where truthful
- Rewrite bullet points to match the JD language
- Highlight the selected projects prominently
- Keep it ATS-friendly
- Do NOT fabricate experience or skills

Return the complete rewritten resume text only."""

    response = client.chat.completions.create(
        model="nvidia/llama-3.3-nemotron-super-49b-v1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000
    )

    state["tailored_resume"] = response.choices[0].message.content.strip()
    return state

# ── Build the LangGraph pipeline ─────────────────────────────────────────────
def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("keyword_diagnostic", keyword_diagnostic_node)
    graph.add_node("project_selector", project_selector_node)
    graph.add_node("resume_modifier", resume_modifier_node)

    graph.set_entry_point("keyword_diagnostic")
    graph.add_edge("keyword_diagnostic", "project_selector")
    graph.add_edge("project_selector", "resume_modifier")
    graph.add_edge("resume_modifier", END)

    return graph.compile()

# ── Main function called by FastAPI ──────────────────────────────────────────
def run_resume_agent(
    job_description: str,
    resume_text: str,
    projects: List[dict] = []
) -> dict:
    agent = build_agent()

    result = agent.invoke({
        "job_description": job_description,
        "resume_text": resume_text,
        "projects": projects,
        "keywords_missing": [],
        "selected_projects": [],
        "tailored_resume": "",
        "diagnostic_report": ""
    })

    return {
        "diagnostic_report": result["diagnostic_report"],
        "missing_keywords": result["keywords_missing"],
        "selected_projects": [p["name"] for p in result["selected_projects"]],
        "tailored_resume": result["tailored_resume"]
    }