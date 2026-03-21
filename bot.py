import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

TOKEN = os.environ.get("TOKEN")

print(f"TOKEN found: {bool(TOKEN)}")

# Flask keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# Minimal bot - no voice, no intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"SUCCESS: Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! Bot is working!")

print("Starting bot...")
bot.run(TOKEN)
