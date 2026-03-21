import discord
import os
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv  # Add this line

# This loads the variables from .env into the script
load_dotenv() 

# Fetch credentials from environment variables
TOKEN = os.environ.get("TOKEN")
# Now this won't be 'None'
CHANNEL_ID = int(os.environ.get("CHANNEL_ID")) 

intents = discord.Intents.default()
intents.voice_states = True  # Add this
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.connect()
        print("Successfully joined the Voice Channel and sitting AFK 24/7.")
    else:
        print("Could not find the Voice Channel. Check your CHANNEL_ID.")

keep_alive()
bot.run(TOKEN)
