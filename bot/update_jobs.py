import json
import requests
from datetime import date

# Demo source (future me real site add karenge)
SOURCE_URL = "https://example.com/jobs.json"

LOCAL_FILE = "jobs.json"

def load_local_jobs():
    try:
        with open(LOCAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_jobs(jobs):
    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

def fetch_new_jobs():
    # Abhi demo job (auto add example)
    return [{
        "id": str(int(date.today().strftime("%Y%m%d"))),
        "title_hi": "नई प्राइवेट भर्ती",
        "title_en": "New Private Job",
        "type": "private",
        "qualification": "10th Pass",
        "age": "18-35",
        "salary": "₹15,000 - 20,000",
        "lastDate": str(date.today()),
        "apply": "https://example.com",
        "details_hi": "नई भर्ती अपने आप जुड़ गई है",
        "details_en": "This job was auto added"
    }]

def main():
    local_jobs = load_local_jobs()
    new_jobs = fetch_new_jobs()

    ids = {job["id"] for job in local_jobs}

    added = False
    for job in new_jobs:
        if job["id"] not in ids:
            local_jobs.append(job)
            added = True

    if added:
        save_jobs(local_jobs)
        print("New job added")
    else:
        print("No new job found")

if __name__ == "__main__":
    main()
