import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

if not TOKEN:
    raise ValueError("TOKEN is missing from environment variables!")
if not CHANNEL_ID:
    raise ValueError("CHANNEL_ID is missing from environment variables!")

CHANNEL_ID = int(CHANNEL_ID)

# Flask keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Discord bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and ONLINE!")

@bot.command(name="afk")
async def afk(ctx):
    """Join the AFK voice channel"""
    channel = bot.get_channel(CHANNEL_ID)
    
    if channel is None:
        await ctx.send("❌ Could not find the voice channel. Check CHANNEL_ID.")
        return

    if not isinstance(channel, discord.VoiceChannel):
        await ctx.send("❌ That channel is not a voice channel.")
        return

    # If already connected, disconnect first
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()

    try:
        await channel.connect()
        await ctx.send("Now sitting AFK in the voice channel 24/7!")
    except Exception as e:
        await ctx.send(f"❌ Failed to join: {e}")
        print(f"Voice connect error: {e}")

@bot.command(name="leave")
async def leave(ctx):
    """Leave the voice channel"""
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("❌ Not in a voice channel.")

keep_alive()
bot.run(TOKEN)
