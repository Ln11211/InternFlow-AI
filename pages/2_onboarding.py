
import streamlit as st
import requests
import json
import PyPDF2
import io

st.set_page_config(
    page_title="InternFlow AI – Setup",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    .stApp { background: #0f0f0f; color: #fff; }
    .section-title {
        color: #76B900;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 4px;
        margin-top: 24px;
    }
    .section-desc { color: #888; font-size: 14px; margin-bottom: 16px; }
    .card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .project-card {
        background: #1e1e1e;
        border: 1px solid #76B900;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

API = "http://127.0.0.1:8000"

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown("<h1 style='color:#76B900;text-align:center'>👋 Let's Set You Up</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;text-align:center'>Tell us about yourself so the AI can personalize everything for you.</p>", unsafe_allow_html=True)

st.markdown("---")

# ── Initialize session state ──────────────────────────────────────────────────
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "projects" not in st.session_state:
    st.session_state.projects = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# ── Section 1: Basic Info ─────────────────────────────────────────────────────
st.markdown("<div class='section-title'>👤 Basic Information</div>", unsafe_allow_html=True)
st.markdown("<div class='section-desc'>This helps personalize your resume and cover letters.</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name", placeholder="e.g. Sreeram Achutuni")
    email = st.text_input("Email", placeholder="e.g. sreeram@sjsu.edu")
    phone = st.text_input("Phone", placeholder="e.g. +1 (408) 123-4567")
with col2:
    university = st.text_input("University", placeholder="e.g. San José State University")
    degree = st.text_input("Degree & Major", placeholder="e.g. MS Data Analytics")
    graduation = st.text_input("Expected Graduation", placeholder="e.g. May 2027")

linkedin = st.text_input("LinkedIn URL", placeholder="https://linkedin.com/in/yourname")
github_profile = st.text_input("GitHub Profile URL", placeholder="https://github.com/yourusername")

st.markdown("---")

# ── Section 2: Target Roles ───────────────────────────────────────────────────
st.markdown("<div class='section-title'>🎯 Target Roles</div>", unsafe_allow_html=True)
st.markdown("<div class='section-desc'>What kinds of internships are you targeting?</div>", unsafe_allow_html=True)

role_options = [
    "ML Engineer", "Data Scientist", "Data Analyst", "Data Engineer",
    "AI Engineer", "Research Engineer", "Software Engineer", "Backend Engineer",
    "Computer Vision Engineer", "NLP Engineer", "Quantitative Analyst"
]
target_roles = st.multiselect("Select your target roles", role_options,
    default=["ML Engineer", "Data Scientist"])
custom_role = st.text_input("Add a custom role (optional)", placeholder="e.g. GenAI Engineer")
if custom_role:
    target_roles.append(custom_role)

preferred_locations = st.multiselect("Preferred Locations",
    ["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
     "Remote", "Boston, MA", "Los Angeles, CA", "Chicago, IL"],
    default=["San Francisco, CA", "Remote"])

st.markdown("---")

# ── Section 3: Resume Upload ──────────────────────────────────────────────────
st.markdown("<div class='section-title'>📄 Upload Your Resume</div>", unsafe_allow_html=True)
st.markdown("<div class='section-desc'>Upload your base resume as a PDF. We'll parse it automatically.</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text() + "\n"
        st.session_state.resume_text = resume_text
        st.success(f"✅ Resume parsed! ({len(pdf_reader.pages)} page(s), {len(resume_text)} characters extracted)")
        with st.expander("Preview extracted text"):
            st.text(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)

        # Auto-save to backend
        resume_name = f"{name}'s Resume" if name else "My Resume"
        try:
            requests.post(f"{API}/resumes/base", json={
                "name": resume_name,
                "content": resume_text,
                "tags": target_roles[:3]
            })
        except:
            pass
    except Exception as e:
        st.error(f"Could not parse PDF: {e}")

st.markdown("---")

# ── Section 4: Projects ───────────────────────────────────────────────────────
st.markdown("<div class='section-title'>🗂️ Your Projects Portfolio</div>", unsafe_allow_html=True)
st.markdown("<div class='section-desc'>Add all your projects — the AI picks the best ones per job automatically.</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🐙 Import from GitHub", "✏️ Add Manually"])

with tab1:
    st.markdown("#### Import projects from your GitHub repos")
    github_url = st.text_input("GitHub Profile or Repo URL",
        placeholder="https://github.com/yourusername",
        key="gh_import")

    if st.button("🔍 Scrape GitHub Projects"):
        if github_url:
            with st.spinner("Fetching your GitHub repos..."):
                try:
                    # Extract username from URL
                    username = github_url.rstrip("/").split("/")[-1]
                    if "github.com" not in github_url:
                        username = github_url

                    # Fetch repos from GitHub API
                    repos_resp = requests.get(
                        f"https://api.github.com/users/{username}/repos?sort=updated&per_page=20",
                        headers={"Accept": "application/vnd.github.v3+json"},
                        timeout=10
                    )

                    if repos_resp.status_code == 200:
                        repos = repos_resp.json()
                        imported = 0

                        for repo in repos:
                            if repo.get("fork"):
                                continue  # Skip forked repos

                            repo_name = repo["name"]
                            description = repo.get("description", "") or ""
                            stars = repo.get("stargazers_count", 0)
                            language = repo.get("language", "Unknown")

                            # Try to fetch README
                            readme_text = ""
                            try:
                                readme_resp = requests.get(
                                    f"https://api.github.com/repos/{username}/{repo_name}/readme",
                                    headers={"Accept": "application/vnd.github.v3.raw"},
                                    timeout=5
                                )
                                if readme_resp.status_code == 200:
                                    readme_text = readme_resp.text[:500]
                            except:
                                pass

                            # Build project description
                            proj_desc = f"{description}. " if description else ""
                            proj_desc += f"Language: {language}. Stars: {stars}. "
                            if readme_text:
                                proj_desc += f"Details: {readme_text[:300]}"

                            # Add to projects if not already there
                            existing_names = [p["name"] for p in st.session_state.projects]
                            if repo_name not in existing_names and proj_desc.strip():
                                st.session_state.projects.append({
                                    "name": repo_name,
                                    "description": proj_desc.strip(),
                                    "source": "github",
                                    "language": language,
                                    "stars": stars
                                })
                                imported += 1

                        st.success(f"✅ Imported {imported} projects from GitHub!")
                        st.rerun()
                    else:
                        st.error(f"Could not fetch repos. Status: {repos_resp.status_code}")
                except Exception as e:
                    st.error(f"GitHub scraping failed: {e}")
        else:
            st.warning("Please enter a GitHub URL")

with tab2:
    st.markdown("#### Add a project manually")
    col1, col2 = st.columns(2)
    with col1:
        proj_name = st.text_input("Project Name",
            placeholder="e.g. PAMAP2 Human Activity Recognition")
    with col2:
        proj_lang = st.text_input("Tech Stack",
            placeholder="e.g. Python, scikit-learn, Streamlit")

    proj_desc = st.text_area("Project Description", height=100,
        placeholder="e.g. Built HAR system using Random Forest on 2.8M records achieving 94.2% accuracy. Deployed on Streamlit Cloud with Git LFS.")

    if st.button("➕ Add Project"):
        if proj_name and proj_desc:
            existing_names = [p["name"] for p in st.session_state.projects]
            if proj_name in existing_names:
                st.warning("Project already exists!")
            else:
                st.session_state.projects.append({
                    "name": proj_name,
                    "description": f"{proj_desc} Tech: {proj_lang}" if proj_lang else proj_desc,
                    "source": "manual",
                    "language": proj_lang,
                    "stars": 0
                })
                st.success(f"✅ Added: {proj_name}")
                st.rerun()
        else:
            st.warning("Please fill in project name and description")

# Show current projects
if st.session_state.projects:
    st.markdown(f"#### Your Projects ({len(st.session_state.projects)})")
    for i, p in enumerate(st.session_state.projects):
        col1, col2 = st.columns([5, 1])
        with col1:
            source_badge = "🐙" if p.get("source") == "github" else "✏️"
            lang = f" · {p.get('language', '')}" if p.get('language') else ""
            stars = f" · ⭐ {p.get('stars', 0)}" if p.get('stars', 0) > 0 else ""
            st.markdown(f"""
            <div class='project-card'>
                <b>{source_badge} {p['name']}</b>{lang}{stars}<br>
                <span style='color:#888;font-size:13px'>{p['description'][:150]}...</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("❌", key=f"rm_proj_{i}"):
                st.session_state.projects.pop(i)
                st.rerun()
else:
    st.info("No projects added yet. Import from GitHub or add manually above.")

st.markdown("---")

# ── Save & Continue ───────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("💾 Save Profile & Browse Jobs →", type="primary", use_container_width=True):
        if not name:
            st.warning("Please enter your name!")
        elif not st.session_state.resume_text and not st.session_state.projects:
            st.warning("Please upload a resume or add at least one project!")
        else:
            # Save profile to session state
            st.session_state.profile = {
                "name": name,
                "email": email,
                "phone": phone,
                "university": university,
                "degree": degree,
                "graduation": graduation,
                "linkedin": linkedin,
                "github": github_profile,
                "target_roles": target_roles,
                "preferred_locations": preferred_locations
            }
            st.success("✅ Profile saved!")
            st.switch_page("pages/3_jobs.py")