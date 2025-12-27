import json, os, re
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")

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

client = TelegramClient("jobbot", API_ID, API_HASH)

def clean(text):
    return re.sub(r"\s+", " ", text).strip()

async def main():
    jobs = []
    if os.path.exists("jobs.json"):
        jobs = json.load(open("jobs.json", "r", encoding="utf-8"))

    titles = {j["title"] for j in jobs}

    for ch in CHANNELS:
        try:
            entity = await client.get_entity(ch)
            history = await client(GetHistoryRequest(
                peer=entity,
                limit=20,
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

                if "apply" in text.lower() or "भर्ती" in text:
                    title = text[:80]
                    if title in titles:
                        continue

                    jobs.append({
                        "title": title,
                        "source": f"https://t.me/{ch}",
                        "details": text,
                        "date": str(msg.date)
                    })
                    titles.add(title)

        except Exception as e:
            print("Error:", ch, e)

    json.dump(jobs, open("jobs.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

with client:
    client.loop.run_until_complete(main())
