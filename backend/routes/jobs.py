import requests
from fastapi import APIRouter

router = APIRouter()

# Simplify Jobs maintains a community-updated JSON of internships
SIMPLIFY_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/.github/scripts/listings.json"

def fetch_listings():
    try:
        response = requests.get(SIMPLIFY_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # Fallback to seed data if GitHub is unreachable
        return get_seed_data()

def get_seed_data():
    """Hardcoded seed data for demo reliability"""
    return [
        {
            "company_name": "Google",
            "title": "Software Engineering Intern - Machine Learning",
            "locations": ["Mountain View, CA"],
            "url": "https://careers.google.com",
            "active": True,
            "date_posted": 1710000000,
            "terms": ["Summer 2025"],
            "sponsorship": "Does Sponsor",
            "description": "Work on ML infrastructure and model training pipelines. Python, TensorFlow, distributed systems experience preferred."
        },
        {
            "company_name": "Meta",
            "title": "Data Science Intern",
            "locations": ["Menlo Park, CA"],
            "url": "https://metacareers.com",
            "active": True,
            "date_posted": 1710000000,
            "terms": ["Summer 2025"],
            "sponsorship": "Does Sponsor",
            "description": "Analyze large-scale datasets to drive product decisions. SQL, Python, A/B testing, statistical modeling required."
        },
        {
            "company_name": "Microsoft",
            "title": "AI/ML Engineering Intern",
            "locations": ["Redmond, WA"],
            "url": "https://careers.microsoft.com",
            "active": True,
            "date_posted": 1710000000,
            "terms": ["Summer 2025"],
            "sponsorship": "Does Sponsor",
            "description": "Build and deploy ML models for Azure AI services. Experience with PyTorch, model optimization, and cloud platforms."
        },
        {
            "company_name": "Netflix",
            "title": "Machine Learning Intern",
            "locations": ["Los Gatos, CA"],
            "url": "https://jobs.netflix.com",
            "active": True,
            "date_posted": 1710000000,
            "terms": ["Summer 2025"],
            "sponsorship": "Does Sponsor",
            "description": "Improve recommendation systems using collaborative filtering, deep learning, and real-time ML pipelines."
        },
        {
            "company_name": "Airbnb",
            "title": "Data Engineering Intern",
            "locations": ["San Francisco, CA"],
            "url": "https://careers.airbnb.com",
            "active": True,
            "date_posted": 1710000000,
            "terms": ["Summer 2025"],
            "sponsorship": "Does Sponsor",
            "description": "Build scalable data pipelines using Spark, Airflow, and Presto. Strong SQL and Python skills required."
        },
        {
            "company_name": "Snap",
            "title": "ML Research Intern",
            "locations": ["Santa Monica, CA"],
            "url": "https://snap.com/jobs",
            "active": True,
            "date_posted": 1710000000,
            "terms": ["Summer 2025"],
            "sponsorship": "Does Sponsor",
            "description": "Research and develop computer vision models for AR features. Experience with CNNs, PyTorch, and real-time inference."
        },
        {
            "company_name": "Uber",
            "title": "Data Science Intern - Marketplace",
            "locations": ["San Francisco, CA"],
            "url": "https://uber.com/careers",
            "active": True,
            "date_posted": 1710000000,
            "terms": ["Summer 2025"],
            "sponsorship": "Does Sponsor",
            "description": "Apply ML to pricing, matching, and demand forecasting problems. Python, SQL, causal inference experience preferred."
        },
        {
            "company_name": "OpenAI",
            "title": "Research Engineer Intern",
            "locations": ["San Francisco, CA"],
            "url": "https://openai.com/careers",
            "active": True,
            "date_posted": 1710000000,
            "terms": ["Summer 2025"],
            "sponsorship": "Does Sponsor",
            "description": "Work on LLM training, RLHF, and evaluation infrastructure. Strong Python, PyTorch, and distributed training skills."
        },
    ]

@router.get("/")
def get_jobs(search: str = "", location: str = "", limit: int = 50):
    listings = fetch_listings()

    results = []
    for job in listings:
        title = job.get("title", "")
        company = job.get("company_name", job.get("company", ""))
        locations = job.get("locations", [])
        active = job.get("active", True)

        if not active:
            continue

        if search:
            if search.lower() not in title.lower() and search.lower() not in company.lower():
                continue

        if location:
            loc_str = " ".join(locations).lower()
            if location.lower() not in loc_str:
                continue

        results.append({
            "id": f"{company}-{title}".replace(" ", "-").lower(),
            "title": title,
            "company": company,
            "locations": locations,
            "url": job.get("url", "#"),
            "date_posted": job.get("date_posted", 0),
            "sponsorship": job.get("sponsorship", "Unknown"),
            "terms": job.get("terms", []),
            "description": job.get("description", "No description available.")
        })

    return {"jobs": results[:limit], "total": len(results)}