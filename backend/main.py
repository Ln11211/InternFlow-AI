from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import jobs, resumes, applications, agent

app = FastAPI(title="InternFlow AI", version="1.0.0")

# Allow Streamlit to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
app.include_router(applications.router, prefix="/applications", tags=["Applications"])
app.include_router(agent.router, prefix="/agent", tags=["AI Agent"])

@app.get("/")
def root():
    return {"message": "InternFlow AI is running!"}