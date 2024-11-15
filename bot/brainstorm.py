import discord
import json

# Load project data from JSON file
with open('resources/projects.json', 'r') as g:
    project_data = json.load(g)

async def brainstorm_commands(message, bot):
    # Ask the user for their preferred programming language
    await message.channel.send('🤖 What programming language are you interested in?')

    # Wait for the user's response
    language_msg = await bot.wait_for(
        'message',
        check=lambda text: text.author == message.author and text.channel == message.channel
    )
    language = language_msg.content.lower()

    # Define available projects based on the language chosen
    project_suggestions = {
        'python': [
            'Data Visualizer', 'Web Scraper', 'AI Chatbot', 'Weather App', 'Portfolio Website'
        ],
        'java': [
            'Expense Tracker', 'Library System', 'Banking App', 'Inventory Manager', 'E-Commerce Site'
        ]
    }

    # Check if the chosen language has any suggested projects
    if language in project_suggestions:
        projects = project_suggestions[language]
        
        # Ask the user to choose a project from the list
        await message.channel.send(
            f'Choose a project:\n- **{projects[0]}** (Beginner)\n- **{projects[1]}** (Intermediate)\n- **{projects[2]}** (Advanced)\n- **{projects[3]}** (Advanced)\n- **{projects[4]}** (Hard)'
        )

        # Wait for the user's project selection
        project_msg = await bot.wait_for(
            'message',
            check=lambda text: text.author == message.author and text.channel == message.channel
        )

        # Get the project details based on the user's choice
        project = project_msg.content.strip().title()
        resource = project_data.get(project)

        # If the selected project exists in the data, display its details
        if resource:
            embed = discord.Embed(
                title=f'📘 {resource["name"]}',
                url=resource['url'],
                description=resource['description'],
                color=discord.Color.green()
            )
            embed.add_field(name='⏳ Project Duration', value=resource['duration'], inline=True)
            embed.add_field(name='🗣️ Programming Language', value=resource['languages'], inline=True)
            embed.add_field(name='💡 Difficulty', value=resource['difficulty'], inline=True)

            await message.channel.send(embed=embed)
        else:
            # If the project is not found, inform the user
            not_found_embed = discord.Embed(
                title='❌ Resource Not Found',
                description=f'Could not find resources for \'{project}\' under {language.capitalize()} projects.',
                color=discord.Color.green()
            )
            await message.channel.send(embed=not_found_embed)
    else:
        # If no projects are available for the chosen language, inform the user
        await message.channel.send(f'❌ No project suggestions available for \'{language}\'.')
