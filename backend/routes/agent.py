from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from agents.resume_agent import run_resume_agent

router = APIRouter()

class Project(BaseModel):
    name: str
    description: str

class AgentRequest(BaseModel):
    job_description: str
    resume_text: str
    projects: Optional[List[Project]] = []

@router.post("/analyze")
def analyze_resume(request: AgentRequest):
    projects = [p.dict() for p in request.projects]
    result = run_resume_agent(
        job_description=request.job_description,
        resume_text=request.resume_text,
        projects=projects
    )
    return result