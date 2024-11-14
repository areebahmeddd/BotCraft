import discord
from utils import get_user_input

async def profile_commands(message, user_profiles, bot):
    command_parts = message.content.split()

    # Check if a subcommand is provided
    if len(command_parts) < 2:
        await message.channel.send('Please provide a subcommand (e.g., `/profile create`, `/profile list`).')
        return

    subcommand = command_parts[1]

    # Sub command: /profile create
    if subcommand == 'create':
        user_id = message.author.id

        # Check if the user already has a profile
        if user_id in user_profiles:
            await message.channel.send('You already have a profile set up. ❌')
            return

        user_profiles[user_id] = {}  # Initialize user's profile data

        # Collect user input for profile fields
        user_profiles[user_id]['name'] = await get_user_input(message, user_id, 'Enter your name 📝:', 'name', bot)
        user_profiles[user_id]['age'] = await get_user_input(message, user_id, 'Got it! Now, enter your age 🎂:', 'age', bot)
        user_profiles[user_id]['role'] = await get_user_input(message, user_id, 'What is your role 👔?', 'role', bot)
        user_profiles[user_id]['interests'] = await get_user_input(message, user_id, 'Tell us about your interests 🎯:', 'interests', bot)
        user_profiles[user_id]['profile_url'] = await get_user_input(message, user_id, "Any profile URL you'd like to share? 🔗:", 'profile_url', bot)
        user_profiles[user_id]['avatar_url'] = await get_user_input(message, user_id, 'Provide an image URL for your avatar 📸:', 'avatar_url', bot)

        # Create and send the profile embed
        profile_embed = discord.Embed(
            title='Profile Successfully Created 🎉',
            color=discord.Color.green()
        )
        for field, value in user_profiles[user_id].items():
            if field != 'avatar_url':  # Skip avatar URL for the fields
                profile_embed.add_field(name=field.capitalize(), value=value, inline=False)
        profile_embed.set_thumbnail(url=user_profiles[user_id]['avatar_url'])

        await message.channel.send(embed=profile_embed)

    # Sub command: /profile list
    elif subcommand == 'list':
        # Check if any profiles exist
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
                profile_embed.set_thumbnail(url=profile.get('avatar_url', ''))

                # Send the profile with a "Connect" button
                await message.channel.send(embed=profile_embed, view=ProfileView(message.author.id, user_id, bot))
        else:
            # Send message if no profiles are found
            no_profiles_embed = discord.Embed(
                title='No Profiles Found 😔',
                description='There are currently no profiles available. Create yours with `/profile create`!',
                color=discord.Color.red()
            )
            await message.channel.send(embed=no_profiles_embed)

class ProfileView(discord.ui.View):
    # Initialize with user and target user IDs
    def __init__(self, user_id, target_user_id, bot):
        super().__init__()
        self.user_id = user_id
        self.target_user_id = target_user_id
        self.bot = bot

    # Handle "Connect" button press
    @discord.ui.button(label='Connect', style=discord.ButtonStyle.primary)
    async def connect_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Send connection request to target user and confirmation to the requester
        target_user = await self.bot.fetch_user(self.target_user_id)
        await target_user.send(f'🔗 {interaction.user.display_name} wants to connect with you!')
        await interaction.response.send_message(f'Your connection request to {target_user.display_name} has been sent! ✅', ephemeral=True)
