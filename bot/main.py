import discord
import os
import json
from dotenv import load_dotenv

from profile import profile_commands
from project import project_commands
from learn import learn_commands

# Load environment variables from .env file
load_dotenv()

# Set up and initialize the bot with intents to access message content
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Dictionaries to store all users' profiles and projects
user_profiles = {}
user_projects = {}

# Load resources from the tutorials.json file
with open('resources/tutorials.json', 'r') as f:
    tutorials = json.load(f)

@bot.event
async def on_ready():
    # Print bot's status once it's online
    print(f'\n[{bot.user.name}] status: Online (ID: {bot.user.id})\n')

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Handle profile commands
    if message.content.startswith('/profile'):
        await profile_commands(message, user_profiles, user_projects, bot)

    # Handle project commands
    elif message.content.startswith('/project'):
        await project_commands(message, user_profiles, user_projects, bot)

    # Handle learn commands
    if message.content.startswith('/learn'):
        await learn_commands(message, tutorials)

bot.run(os.getenv('DISCORD_TOKEN'))
