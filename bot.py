import discord
from discord.ext import commands, tasks
import os
from flask import Flask
from threading import Thread

# --- Dummy Web Server for UptimeRobot ---
app = Flask('')
@app.route('/')
def home():
    return "AFK Bot is online and keeping the VC alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

# --- Discord Bot Setup ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ⚠️ REPLACE THIS WITH YOUR ACTUAL VOICE CHANNEL ID
VC_CHANNEL_ID = 1000483926135029782 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    check_vc.start() # Starts the loop to make sure it never drops

# This loop checks every 5 minutes to ensure the bot is still in the VC.
# If Discord randomly disconnects it, the bot will instantly rejoin.
@tasks.loop(minutes=5)
async def check_vc():
    channel = bot.get_channel(VC_CHANNEL_ID)
    
    # If the bot is not currently in a voice channel, connect to it
    if not bot.voice_clients:
        vc = await channel.connect()
        # Muting and deafening the bot saves bandwidth and stops Discord from kicking it for being idle
        await vc.guild.change_voice_state(channel=channel, self_mute=True, self_deaf=True)
        print("Reconnected to VC and went AFK!")

# Start the web server and the bot
Thread(target=run).start()
bot.run(os.getenv('TOKEN'))
