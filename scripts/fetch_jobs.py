import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

JOBS_FILE = "jobs.json"

def load_jobs():
    try:
        with open(JOBS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_jobs(jobs):
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

def job_exists(jobs, title):
    return any(job["title"] == title for job in jobs)

def fetch_example_jobs():
    jobs = []

    url = "https://www.freejobalert.com/latest-notifications/"
    r = requests.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("table tbody tr")[:5]

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            title = cols[0].get_text(strip=True)
            link = cols[0].find("a")["href"]

            jobs.append({
                "id": int(datetime.now().timestamp()),
                "title": title,
                "type": "Government",
                "mode": "Online",
                "location": "India",
                "lastDate": "Check Notification",
                "details": "Auto fetched job (no captcha source)",
                "applyLink": link
            })
    return jobs

def main():
    existing_jobs = load_jobs()
    new_jobs = fetch_example_jobs()

    for job in new_jobs:
        if not job_exists(existing_jobs, job["title"]):
            existing_jobs.append(job)

    save_jobs(existing_jobs)

if __name__ == "__main__":
    main()
