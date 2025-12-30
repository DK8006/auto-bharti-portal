import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://sarkarialert.net/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_jobs():
    res = requests.get(URL, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []
    job_id = 1

    # Latest Jobs section boxes
    boxes = soup.select("div.latest-jobs a")

    for a in boxes:
        title = a.get_text(strip=True)
        link = a.get("href")

        if not link.startswith("http"):
            link = URL.rstrip("/") + "/" + link.lstrip("/")

        jobs.append({
            "id": job_id,
            "title": title,
            "department": "Sarkari Result",
            "last_date": "Check Notification",
            "apply_link": link,
            "source": "sarkarialert.net",
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        job_id += 1

    return jobs

if __name__ == "__main__":
    jobs = fetch_jobs()

    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(jobs)} jobs updated")
