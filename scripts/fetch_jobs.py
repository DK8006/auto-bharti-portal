import json
import feedparser
from datetime import datetime

JOBS_FILE = "jobs.json"

RSS_SOURCES = [
    {
        "name": "Employment News",
        "url": "https://www.employmentnews.gov.in/NewEmp/RSS.xml"
    }
]

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
    return any(title.lower() == job["title"].lower() for job in jobs)

def fetch_from_rss():
    jobs = []
    for src in RSS_SOURCES:
        feed = feedparser.parse(src["url"])
        for entry in feed.entries[:10]:
            jobs.append({
                "id": int(datetime.now().timestamp() * 1000),
                "title": entry.title,
                "type": "Government",
                "mode": "Online",
                "location": "India",
                "lastDate": "Check Notification",
                "details": entry.summary if "summary" in entry else "Official RSS source",
                "applyLink": entry.link
            })
    return jobs

def main():
    existing_jobs = load_jobs()
    new_jobs = fetch_from_rss()

    added = 0
    for job in new_jobs:
        if not job_exists(existing_jobs, job["title"]):
            existing_jobs.append(job)
            added += 1

    if added > 0:
        save_jobs(existing_jobs)

if __name__ == "__main__":
    main()
