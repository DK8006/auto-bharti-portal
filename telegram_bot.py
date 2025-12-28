import json
import os
import re
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# --- Telegram credentials from GitHub Secrets ---
API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH")
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

# Basic safety checks
if API_ID == 0 or not API_HASH:
    raise ValueError("TG_API_ID or TG_API_HASH missing")
if not BOT_TOKEN:
    raise ValueError("TG_BOT_TOKEN missing")

# --- Telegram client using bot token ---
client = TelegramClient(
    "jobbot",
    API_ID,
    API_HASH
).start(bot_token=BOT_TOKEN)

# --- Channels to read ---
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

# --- helper to clean text ---
def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

# --- main async function ---
async def main():
    # ensure client is started (already started above)
    # gather existing jobs
    jobs = []
    if os.path.exists("jobs.json"):
        try:
            jobs = json.load(open("jobs.json", "r", encoding="utf-8"))
        except:
            jobs = []

    # build a set of existing titles to avoid duplicates
    titles = {j.get("title", "") for j in jobs}

    # iterate over channels
    for ch in CHANNELS:
        try:
            entity = await client.get_entity(ch)
            history = await client(GetHistoryRequest(
                peer=entity,
                limit=100,          # read up to 100 recent messages
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

                # stronger keyword check: govt/private job words
                if any(word in text.lower() for word in [
                    "apply", "bharti", "vacancy", "recruitment",
                    "job", "भर्ती", "नौकरी", "रिक्रूट", "आवश्यक", "भर्ती"
                ]):
                    # use first line up to 120 chars as title
                    title = text.split("\n")[0][:120]

                    if title in titles:
                        continue

                    # add job item
                    jobs.append({
                        "title": title,
                        "source": f"https://t.me/{ch}",
                        "details": text,
                        "date": str(msg.date)
                    })
                    titles.add(title)

        except Exception as e:
            # just print error; continue to next channel
            print("Error:", ch, e)

    # save updated jobs
    try:
        json.dump(jobs, open("jobs.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    except Exception as e:
        print("Error saving jobs:", e)

# --- run the async function ---
with client:
    client.loop.run_until_complete(main())
