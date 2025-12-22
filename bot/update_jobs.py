import json
from datetime import datetime

JOBS_FILE = "jobs.json"
SOURCES_FILE = "bot/sources.json"

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def remove_expired(jobs):
    today = datetime.today().strftime("%Y-%m-%d")
    return [j for j in jobs if j.get("lastDate", today) >= today]

def generate_demo_jobs(sources):
    jobs = []
    today = datetime.today().strftime("%Y-%m-%d")

    for src in sources:
        jid = f"{src['name'].lower().replace(' ','-')}-{today}"
        jobs.append({
            "id": jid,
            "title_hi": f"{src['name']} नई भर्ती",
            "title_en": f"{src['name']} New Recruitment",
            "type": src["type"],
            "qualification": "10th / 12th / Graduate",
            "age": "18-35",
            "salary": "As per rules",
            "lastDate": today,
            "apply": src["url"],
            "details_hi": f"{src['name']} से नई भर्ती auto add हुई है",
            "details_en": f"Auto-added job from {src['name']}"
        })
    return jobs

def main():
    jobs = load_json(JOBS_FILE, [])
    sources = load_json(SOURCES_FILE, [])

    jobs = remove_expired(jobs)
    existing_ids = {j["id"] for j in jobs}

    new_jobs = generate_demo_jobs(sources)

    added = False
    for j in new_jobs:
        if j["id"] not in existing_ids:
            jobs.append(j)
            added = True

    if added:
        save_json(JOBS_FILE, jobs)
        print("Jobs updated from sources")
    else:
        print("No new jobs found")

if __name__ == "__main__":
    main()
