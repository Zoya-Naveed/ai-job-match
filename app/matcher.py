import requests

ADZUNA_APP_ID = "36ba703f"
ADZUNA_APP_KEY = "04bab1e4bdf47ddabde9711236f86a27"
ADZUNA_API_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

def match_jobs(skills):
    print(f"Matching jobs for skills: {skills}")
    query = " ".join(skills)
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": query,
        "results_per_page": 5,
        "content-type": "application/json",
        "sort_by": "relevance",
        "distance": 25,
        "max_days_old": 30
    }
    response = requests.get(ADZUNA_API_URL, params=params)
    print("API status code:", response.status_code)
    if response.status_code != 200:
        print("API error:", response.text)
        return []
    data = response.json()
    print("Jobs found:", len(data.get("results", [])))
    jobs = []
    for job in data.get("results", []):
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "redirect_url": job.get("redirect_url"),
            "match_score": 100
        })
    return jobs
