# import
import db
import os
import time
import json
import discord
import logging
from dotenv import load_dotenv
from functions import background
from discord.ext import commands
from functions import leaderboard_func

#DEBUG
import tracemalloc
tracemalloc.start()

# Initialize
db.initialize()
db.last_message_time = int(time.time()) - 86400

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# environment variables
load_dotenv()
TOKEN = os.getenv('discord_token')
PREFIX = os.getenv('prefix')

intents = discord.Intents.default()
intents.members = True

description = '''
Kalendar Bot zur Terminerstellung und -verfolgung.
Schickt x Erinnerungen vor jedem Termin:
- 2 für fehlende votes
- 1 3h vorher für maybe votes
- 1 kurz vorher für positive Eintragung
Sagt bei 5 positiven Votes, dass der Termin feststeht.
Rolle 'Terminerinnerung' kann für Urlaub entfernt werden.
Elo gibts für Erinnerungen bei fehlenden Votes und maybes.
'''
bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX), description=description, intents=intents) #, help_command = None)

print('> Loading Commandclasses')
for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{os.path.splitext(filename)[0]}')
        print(f'{os.path.splitext(filename)[0]} loaded')
print()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('-'*30)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{PREFIX}help'))

    db.bot = bot

    try:
        json.load( open( "leaderboard.json" ) )
    except:
        leaderboard_func.init_leaderboard()

    await background.BackgroundTasks().initialize()
    

bot.run(TOKEN)