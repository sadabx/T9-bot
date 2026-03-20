import discord
import os
from discord.ext import commands
from keep_alive import keep_alive

# Fetch credentials from environment variables
TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID")) 

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    # Find the voice channel
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # Connect to the channel and just stay there
        await channel.connect()
        print("Successfully joined the Voice Channel and sitting AFK 24/7.")
    else:
        print("Could not find the Voice Channel. Check your CHANNEL_ID.")

# Start the web server for UptimeRobot
keep_alive()

# Run the bot
bot.run(TOKEN)