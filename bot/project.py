import discord
from utils import get_user_input

async def project_commands(message, user_profiles, user_projects, bot):
    command_parts = message.content.split()

    if len(command_parts) < 2:
        await message.channel.send("Please provide a subcommand (e.g., `/project create`, `/project list`).")
        return

    subcommand = command_parts[1]

    # Sub command: /project create
    if subcommand == "create":
        user_id = message.author.id

        # Ensure the user has a profile set up before they can create a project
        if user_id not in user_profiles:
            await message.channel.send("You need to set up your profile first using `/profile setup`.")
            return

        # Initialize the user's project dictionary if it doesn't exist
        if user_id not in user_projects:
            user_projects[user_id] = []

        # Get project details from the user
        project_name = await get_user_input(message, user_id, "What is the name of your project? 📝", 'name', bot)
        project_description = await get_user_input(message, user_id, "Please provide a description of your project 📜", 'description', bot)
        project_status = await get_user_input(message, user_id, "What is the current status of the project? (e.g., 'Planning', 'In Progress', 'Completed') ⚙️", 'status', bot)
        project_theme = await get_user_input(message, user_id, "What is the theme of the project? 🎨", 'theme', bot)
        project_tech_stack = await get_user_input(message, user_id, "Please list the tech stack for the project 💻", 'tech_stack', bot)
        project_mentors = await get_user_input(message, user_id, "Please list your mentors for this project (separate by commas) 👨‍🏫", 'mentors', bot)

        # Create the project entry
        project = {
            'name': project_name,
            'description': project_description,
            'status': project_status,
            'theme': project_theme,
            'tech_stack': project_tech_stack,
            'mentors': project_mentors.split(','),
        }

        # Add the project to the user's project list
        user_projects[user_id].append(project)

        # Send a confirmation message with the project details
        project_embed = discord.Embed(
            title=f"Project {project_name} Created! 🎉",
            description=project_description,
            color=discord.Color.green()
        )
        project_embed.add_field(name="Status", value=project_status, inline=True)
        project_embed.add_field(name="Theme", value=project_theme, inline=True)
        project_embed.add_field(name="Tech Stack", value=project_tech_stack, inline=True)
        project_embed.add_field(name="Mentors", value=", ".join(project['mentors']), inline=True)

        await message.channel.send(embed=project_embed)

    # Sub command: /project list
    elif subcommand == "list":
        user_id = message.author.id

        # Check if the user has any projects
        if user_id not in user_projects or not user_projects[user_id]:
            await message.channel.send("You have no projects listed. Create one using `/project create`!")
            return

        # List all the user's projects
        for project in user_projects[user_id]:
            project_embed = discord.Embed(
                title=f"{project['name']} 📂",
                description=project['description'],
                color=discord.Color.blue()
            )
            project_embed.add_field(name="Status", value=project['status'], inline=False)
            project_embed.add_field(name="Theme", value=project['theme'], inline=False)
            project_embed.add_field(name="Tech Stack", value=project['tech_stack'], inline=False)
            project_embed.add_field(name="Mentors", value=", ".join(project['mentors']), inline=False)

            # Add the "Notify Me" button to each project
            view = discord.ui.View()
            notify_button = discord.ui.Button(label="Notify Me", style=discord.ButtonStyle.primary)

            async def notify_callback(interaction: discord.Interaction):
                # Notify the user (or the project's creator)
                await interaction.response.send_message(f"You will be notified about updates on the project: {project['name']}! ✅", ephemeral=True)

            notify_button.callback = notify_callback
            view.add_item(notify_button)

            # Send the project embed with the button
            await message.channel.send(embed=project_embed, view=view)
