import discord
import os
from dotenv import load_dotenv

from profile import profile_commands
from project import project_commands

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# Dictionary to store all users' profiles
user_profiles = {}

# Dictionary to store all users' projects
user_projects = {}

@bot.event
async def on_ready():
    print(f'\n[{bot.user.name}] status: Online (ID: {bot.user.id})\n')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Handle profile commands
    if message.content.startswith("/profile"):
        await profile_commands(message, user_profiles, user_projects, bot)

    # Handle project commands
    elif message.content.startswith("/project"):
        await project_commands(message, user_profiles, user_projects, bot)

bot.run(os.getenv('DISCORD_TOKEN'))
