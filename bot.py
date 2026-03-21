import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# Validate env vars early so we get a clear error
if not TOKEN:
    raise ValueError("TOKEN is missing from environment variables!")
if not CHANNEL_ID:
    raise ValueError("CHANNEL_ID is missing from environment variables!")

CHANNEL_ID = int(CHANNEL_ID)

# Flask keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and sitting AFK 24/7."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Discord bot
intents = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    print(f"Channel found: {channel}")
    print(f"Channel type: {type(channel)}")
    if isinstance(channel, discord.VoiceChannel):
        try:
            await channel.connect()
            print("Successfully joined the Voice Channel.")
        except Exception as e:
            print(f"Failed to connect to voice channel: {e}")
    else:
        print(f"Channel is not a VoiceChannel or not found. CHANNEL_ID={CHANNEL_ID}")

keep_alive()
bot.run(TOKEN)
