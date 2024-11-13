import discord
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# Dictionary to temporarily store profile info during setup
user_profiles = {}

@bot.event
async def on_ready():
    print(f'\n[{bot.user.name}] status: Online (ID: {bot.user.id})\n')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("/profile setup"):
        user_id = message.author.id
        user_profiles[user_id] = {}

        await message.channel.send("Please enter your name:")

        def check_name(m):
            return m.author.id == user_id and m.channel == message.channel

        name_msg = await bot.wait_for("message", check=check_name)
        user_profiles[user_id]['name'] = name_msg.content
        await message.channel.send("Got it! Now please enter your age:")

        def check_age(m):
            return m.author.id == user_id and m.channel == message.channel

        age_msg = await bot.wait_for("message", check=check_age)
        user_profiles[user_id]['age'] = age_msg.content
        await message.channel.send("Great! Now, tell us about your interests:")

        def check_interests(m):
            return m.author.id == user_id and m.channel == message.channel

        interests_msg = await bot.wait_for("message", check=check_interests)
        user_profiles[user_id]['interests'] = interests_msg.content
        await message.channel.send("Awesome! Please provide a link to your profile URL.")

        def check_url(m):
            return m.author.id == user_id and m.channel == message.channel

        url_msg = await bot.wait_for("message", check=check_url)
        user_profiles[user_id]['profile_url'] = url_msg.content
        await message.channel.send("Lastly, provide an image URL for your avatar (e.g., a .jpg or .png link):")

        def check_avatar(m):
            return m.author.id == user_id and m.channel == message.channel

        avatar_msg = await bot.wait_for("message", check=check_avatar)
        user_profiles[user_id]['avatar_url'] = avatar_msg.content

        profile_embed = discord.Embed(
            title="Profile Successfully Created",
            color=discord.Color.blue()
        )
        profile_embed.add_field(name="Name", value=user_profiles[user_id]['name'], inline=False)
        profile_embed.add_field(name="Age", value=user_profiles[user_id]['age'], inline=False)
        profile_embed.add_field(name="Interests", value=user_profiles[user_id]['interests'], inline=False)
        profile_embed.add_field(name="Profile URL", value=user_profiles[user_id]['profile_url'], inline=False)
        profile_embed.set_thumbnail(url=user_profiles[user_id]['avatar_url'])
        profile_embed.set_footer(text=f"Profile for {message.author.display_name}")

        await message.channel.send(embed=profile_embed)

        user_profiles.pop(user_id)

bot.run(os.getenv('DISCORD_TOKEN'))
