import os
import re
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# --- Telegram credentials (GitHub Secrets se aayenge) ---
API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH")
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

if API_ID == 0 or not API_HASH or not BOT_TOKEN:
    raise ValueError("Telegram API credentials missing")

# --- Telegram client ---
client = TelegramClient(
    "jobbot",
    API_ID,
    API_HASH
).start(bot_token=BOT_TOKEN)

# --- Channels to read (IMAGE WALE + PEHLE WALE SAB ADD) ---
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

# --- helper: text clean ---
def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

# --- main async function ---
async def main():
    for channel in CHANNELS:
        print(f"\n📢 Reading from: {channel}")
        try:
            entity = await client.get_entity(channel)

            history = await client(GetHistoryRequest(
                peer=entity,
                limit=100,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))

            for msg in history.messages:
                if msg.message:
                    print("➡️", clean(msg.message)[:200])

        except Exception as e:
            print(f"❌ Error in {channel}: {e}")

with client:
    client.loop.run_until_complete(main())
