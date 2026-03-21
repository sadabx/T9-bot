import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

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
    if channel:
        await channel.connect()
        print("Successfully joined the Voice Channel.")
    else:
        print("Could not find the Voice Channel. Check your CHANNEL_ID.")

keep_alive()
bot.run(TOKEN)
