import os
import json
import re
import asyncio
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.functions.messages 
import GetHistoryRequest
from datetime import datetime

def normalize_date(date_str):
    if not date_str:
        return "Check Notification"

    date_str = date_str.strip()

    formats = [
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d %b %Y",
        "%d %B %Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%d-%m-%Y")
        except:
            pass

    return "Check Notification"

# ================== ENV ==================
API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH")
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

if API_ID == 0 or not API_HASH or not BOT_TOKEN:
    raise ValueError("TG_API_ID / TG_API_HASH / TG_BOT_TOKEN missing")

# ================== CLIENT ==================
client = TelegramClient(
    "jobbot",
    API_ID,
    API_HASH
).start(bot_token=BOT_TOKEN)

# ================== CHANNELS ==================
CHANNELS = [
    "SarkariResultOfficial",
    "GovtJobsAlert",
    "rojgar_result",
    "FreeJobAlertOfficial",
    "UPBhartiUpdates",
    "LatestGovtJobsHindi",
    "OutsourceJobsIndia",
    "ITI_Jobs",
    "10th12thJobs"
]

LIMIT = 100  # 👈 posts limit

# ================== HELPERS ==================
def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def parse_job(text: str):
    t = text.lower()

    # Department
    department = "Other"
    if "ssc" in t:
        department = "SSC"
    elif "upsssc" in t:
        department = "UPSSSC"
    elif "railway" in t or "rrb" in t:
        department = "Railway"
    elif "outsour" in t or "contract" in t:
        department = "Outsourcing"

    # Post
    post = "Various Posts"
    for p in [
        "gd constable", "chsl", "mts", "cgl",
        "stenographer", "je", "technician",
        "helper", "clerk", "assistant"
    ]:
        if p in t:
            post = p.upper()
            break

    # Last Date
last_date = "Check Notification"

patterns = [
    r"(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
    r"(\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4})"
]

for p in patterns:
    m = re.search(p, text, re.IGNORECASE)
    if m:
        last_date = normalize_date(m.group(1))
        break

# ================== MAIN ==================
async def main():
    jobs = []

    # load existing jobs.json
    if os.path.exists("jobs.json"):
        with open("jobs.json", "r", encoding="utf-8") as f:
            jobs = json.load(f)

    existing_ids = {j["id"] for j in jobs}

    for ch in CHANNELS:
        try:
            entity = await client.get_entity(ch)
            history = await client(GetHistoryRequest(
                peer=entity,
                limit=LIMIT,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))

            for msg in history.messages:
                if not msg.message:
                    continue

                text = clean(msg.message)
                department, post, last_date = parse_job(text)

                job_id = f"{department.lower()}-{msg.id}"

                if job_id in existing_ids:
                    continue

                job = {
                    "id": job_id,
                    "title_hi": f"{department} – {post}",
                    "title_en": f"{department} – {post}",
                    "type": "government" if department != "Outsourcing" else "outsourcing",
                    "department": department,
                    "post": post,
                    "qualification": "As per notification",
                    "age": "As per rules",
                    "salary": "As per rules",
                    "lastDate": last_date or "Check Notification",
                    "apply": "Check Notification",
                    "details_hi": text[:300],
                    "details_en": text[:300]
                }

                jobs.append(job)
                existing_ids.add(job_id)

        except Exception as e:
            print(f"Error in channel {ch}: {e}")

    # save jobs.json
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

# ================== RUN ==================
asyncio.run(main())
