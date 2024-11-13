import discord
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# Dictionary to store all users' profiles
user_profiles = {}

class ProfileView(discord.ui.View):
    # Initialize with user and target user IDs
    def __init__(self, user_id, target_user_id):
        super().__init__()
        self.user_id = user_id
        self.target_user_id = target_user_id

    # Handle "Connect" button press
    @discord.ui.button(label="Connect", style=discord.ButtonStyle.primary)
    async def connect_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Send connection request to target user and confirmation to the requester
        target_user = await bot.fetch_user(self.target_user_id)
        await target_user.send(f"🔗 {interaction.user.display_name} wants to connect with you!")
        await interaction.response.send_message(f"Your connection request to {target_user.display_name} has been sent! ✅", ephemeral=True)

@bot.event
async def on_ready():
    print(f'\n[{bot.user.name}] status: Online (ID: {bot.user.id})\n')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Parent command: /profile
    if message.content.startswith("/profile"):
        command_parts = message.content.split()

        if len(command_parts) < 2:
            await message.channel.send("Please provide a subcommand (e.g., `/profile setup`, `/profile list`).")
            return

        subcommand = command_parts[1]

        # Sub command: /profile setup
        if subcommand == "setup":
            user_id = message.author.id

            if user_id in user_profiles:
                await message.channel.send("You already have a profile set up. ❌")
                return

            user_profiles[user_id] = {}  # Initialize user's profile data

            # Get user inputs using the get_user_input function
            user_profiles[user_id]['name'] = await get_user_input(message, user_id, "Please enter your name 📝:", 'name')
            user_profiles[user_id]['age'] = await get_user_input(message, user_id, "Got it! Now, please enter your age 🎂:", 'age')
            user_profiles[user_id]['role'] = await get_user_input(message, user_id, "What is your role 👔?", 'role')
            user_profiles[user_id]['interests'] = await get_user_input(message, user_id, "Now, tell us about your interests 🎯:", 'interests')
            user_profiles[user_id]['profile_url'] = await get_user_input(message, user_id, "Please provide a link to your profile URL 🌐:", 'profile_url')
            user_profiles[user_id]['avatar_url'] = await get_user_input(message, user_id, "Lastly, provide an image URL for your avatar (e.g., a .jpg or .png link) 📸:", 'avatar_url')

            # Create and send the profile embed
            profile_embed = discord.Embed(
                title="Profile Successfully Created 🎉",
                color=discord.Color.green()
            )
            for field, value in user_profiles[user_id].items():
                if field != 'avatar_url':  # Skip avatar URL for the fields
                    profile_embed.add_field(name=field.capitalize(), value=value, inline=False)
            profile_embed.set_thumbnail(url=user_profiles[user_id]['avatar_url'])
            profile_embed.set_footer(text=f"Profile for {message.author.display_name}")

            await message.channel.send(embed=profile_embed)

        # Sub command: /profile list
        elif subcommand == "list":
            if user_profiles:
                for user_id, profile in user_profiles.items():
                    user = await bot.fetch_user(user_id)
                    profile_embed = discord.Embed(
                        title=f"{user.display_name}'s Profile 👤",
                        color=discord.Color.blue()
                    )
                    for field, value in profile.items():
                        if field != 'avatar_url':  # Skip avatar URL for the fields
                            profile_embed.add_field(name=field.capitalize(), value=value, inline=False)
                    profile_embed.set_thumbnail(url=profile.get("avatar_url", ""))

                    # Send the embed with a "Connect" button using ProfileView
                    await message.channel.send(embed=profile_embed, view=ProfileView(message.author.id, user_id))

            else:
                no_profiles_embed = discord.Embed(
                    title="No Profiles Found 😔",
                    description="There are currently no profiles available. Create yours with `/profile setup`!",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=no_profiles_embed)

# Helper function to collect user input
async def get_user_input(message, user_id, prompt, field_name):
    # Send prompt and wait for user response
    await message.channel.send(prompt)
    def check(m):
        return m.author.id == user_id and m.channel == message.channel
    response = await bot.wait_for("message", check=check)
    return response.content

bot.run(os.getenv('DISCORD_TOKEN'))
