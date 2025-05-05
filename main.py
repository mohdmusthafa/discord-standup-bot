import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler

type(load_dotenv())

CHANNEL_ID = os.getenv("CHANNEL_ID")
TIMEZONE = os.getenv("TIMEZONE", "UTC")
POLL_HOUR = os.getenv("POLL_HOUR")
POLL_MINUTE = os.getenv("POLL_MINUTE")
TOKEN = os.getenv("TOKEN")


intents = discord.Intents.default()
client = discord.Client(intents=intents)

scheduler = AsyncIOScheduler()

async def send_poll():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        channel = await client.fetch_channel(CHANNEL_ID)


    embed = discord.Embed(
        title="Daily Standup Poll",
        description="Can you join today's standup at 9:15 PM? \n\n" \
        "👍 Yes | 👎 No",
        color=0x00AE86
    )

    await channel.send(embed=embed)

    print(f"[Poll] Sent at {datetime.now(pytz.timezone(TIMEZONE)).isoformat()}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    scheduler.add_job(
        send_poll,
        'cron',
        hour=POLL_HOUR,
        minute=POLL_MINUTE
    )
    scheduler.start()
    print(f"Scheduled daily poll at {POLL_HOUR}:{POLL_MINUTE} {TIMEZONE}")

if __name__ == "__main__":
    client.run(TOKEN)