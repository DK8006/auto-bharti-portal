import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

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
    return any(title.lower() == job["title"].lower() for job in jobs)

def fetch_freejobalert():
    collected = []
    base_url = "https://www.freejobalert.com/latest-notifications/page/"

    for page in range(1, 4):  # 3 pages = ~15 jobs
        try:
            r = requests.get(base_url + str(page), timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            rows = soup.select("table tbody tr")

            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    title = cols[0].get_text(strip=True)
                    link = cols[0].find("a")["href"]

                    collected.append({
                        "id": int(datetime.now().timestamp() * 1000),
                        "title": title,
                        "type": "Government",
                        "mode": "Online",
                        "location": "India",
                        "lastDate": "Check Notification",
                        "details": "Auto fetched (no captcha source)",
                        "applyLink": link
                    })
            time.sleep(2)
        except:
            continue

    return collected

def main():
    jobs = load_jobs()
    new_jobs = fetch_freejobalert()
    added = 0

    for job in new_jobs:
        if not job_exists(jobs, job["title"]):
            jobs.append(job)
            added += 1

    if added > 0:
        save_jobs(jobs)

if __name__ == "__main__":
    main()
