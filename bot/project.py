import discord
from utils import get_user_input

async def project_commands(message, user_profiles, user_projects, bot):
    command_parts = message.content.split()

    # Check if a subcommand is provided
    if len(command_parts) < 2:
        await message.channel.send('Please provide a subcommand (e.g., `/project create`, `/project list`).')
        return

    subcommand = command_parts[1]

    # Sub command: /project create
    if subcommand == 'create':
        user_id = message.author.id

        # Ensure the user has a profile set up before creating a project
        if user_id not in user_profiles:
            await message.channel.send('You need to set up your profile first using `/profile create`.')
            return

        # Initialize user's projects if it doesn't exist
        if user_id not in user_projects:
            user_projects[user_id] = []

        project = {} # Initialize project data

        # Collect user input for each project field
        project['name'] = await get_user_input(message, user_id, 'Name of your project? 📝', 'name', bot)
        project['description'] = await get_user_input(message, user_id, 'Description of your project 📜', 'description', bot)
        project['status'] = await get_user_input(message, user_id, 'Current status of the project? ⚙️', 'status', bot)
        project['theme'] = await get_user_input(message, user_id, 'Theme of the project? 🎨', 'theme', bot)
        project['tech_stack'] = await get_user_input(message, user_id, 'Tech stack 💻', 'tech_stack', bot)
        project['mentors'] = (await get_user_input(message, user_id, 'Mentors 👨‍🏫', 'mentors', bot)).split(',')

        # Add the project to the user's project list
        user_projects[user_id].append(project)

        # Create and send confirmation embed
        project_embed = discord.Embed(
            title=f'Project {project["name"]} Created! 🎉',
            description=project['description'],
            color=discord.Color.green()
        )
        project_embed.add_field(name='Status', value=project['status'], inline=True)
        project_embed.add_field(name='Theme', value=project['theme'], inline=True)
        project_embed.add_field(name='Tech Stack', value=project['tech_stack'], inline=True)
        project_embed.add_field(name='Mentors', value=', '.join(project['mentors']), inline=True)

        await message.channel.send(embed=project_embed)

    # Sub command: /project list
    elif subcommand == 'list':
        user_id = message.author.id

        # Check if the user has any projects
        if user_id not in user_projects or not user_projects[user_id]:
            await message.channel.send('You have no projects. Create one using `/project create`!')
            return

        # List all projects of the user
        for project in user_projects[user_id]:
            project_embed = discord.Embed(
                title=f'{project["name"]} 📂',
                description=project['description'],
                color=discord.Color.blue()
            )
            project_embed.add_field(name='Status', value=project['status'], inline=False)
            project_embed.add_field(name='Theme', value=project['theme'], inline=False)
            project_embed.add_field(name='Tech Stack', value=project['tech_stack'], inline=False)
            project_embed.add_field(name='Mentors', value=', '.join(project['mentors']), inline=False)

            # Add "Notify Me" button for each project
            view = discord.ui.View()
            notify_button = discord.ui.Button(label='Notify Me', style=discord.ButtonStyle.primary)

            # Callback for notify button click
            async def notify_callback(interaction: discord.Interaction):
                await interaction.response.send_message(f'You will be notified about updates on the project: {project["name"]}! ✅', ephemeral=True)

            notify_button.callback = notify_callback
            view.add_item(notify_button)

            # Send the embed with the button
            await message.channel.send(embed=project_embed, view=view)
