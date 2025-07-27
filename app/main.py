from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from .resume_parser import extract_skills
from .matcher import match_jobs

# Get correct base path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()




# Mount static and templates with full path
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse("index.html", {"request": request, "results": None})

@app.post("/match_jobs", response_class=HTMLResponse)
async def match_jobs_from_resume(request: Request, resume_file: UploadFile = File(...)):
    contents = await resume_file.read()
    text = contents.decode("utf-8")
    print("Uploaded resume text:", text[:200])  # print first 200 chars

    skills = extract_skills(text)
    print("Extracted skills:", skills)

    if not skills:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": [],
            "error": "No skills detected in your resume."
        })

    job_matches = match_jobs(skills)
    print("Jobs matched:", job_matches)

    if not job_matches:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": [],
            "error": "No matching jobs found for your skills."
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": job_matches,
        "error": None
    })
