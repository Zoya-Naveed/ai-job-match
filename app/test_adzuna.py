import requests

ADZUNA_APP_ID = "36ba703f"
ADZUNA_APP_KEY = "04bab1e4bdf47ddabde9711236f86a27"
ADZUNA_API_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

def test_adzuna_api():
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": "python docker",
        "results_per_page": 5,
        "content-type": "application/json",
        "sort_by": "relevance",
        "distance": 25,
        "max_days_old": 30
    }
    response = requests.get(ADZUNA_API_URL, params=params)
    print("Status code:", response.status_code)
    data = response.json()
    print("Response JSON keys:", data.keys())
    print("Number of jobs returned:", len(data.get("results", [])))
    for job in data.get("results", []):
        print(f"{job.get('title')} at {job.get('company', {}).get('display_name')} - {job.get('redirect_url')}")

if __name__ == "__main__":
    test_adzuna_api()
