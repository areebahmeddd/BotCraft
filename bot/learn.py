import discord
import json

# Load tutorials data from JSON file
with open('resources/tutorials.json', 'r') as f:
    tutorials = json.load(f)

async def learn_commands(message):
    command_parts = message.content.split(maxsplit=2)

    # Check if a subcommand is provided
    if len(command_parts) == 2:
        language = command_parts[1].lower()

        # Sub command: /learn <language>
        if language in tutorials:
            tutorial_list = tutorials[language]
            embed = discord.Embed(
                title=f'{language.capitalize()} Tutorials',
                description=f'A list of useful tutorials for {language.capitalize()}.',
                color=discord.Color.blue()
            )

            # Add each tutorial to the embed as a field
            for index, tutorial in enumerate(tutorial_list, start=1):
                embed.add_field(name=f'Tutorial {index}', value=tutorial['course_name'], inline=False)

            await message.channel.send(embed=embed)
        else:
            # Error: No tutorials found for the specified language
            error_embed = discord.Embed(
                title='🔍 Language Not Found',
                description=f"Sorry, I don't have any tutorials for '{language}'.",
                color=discord.Color.red()
            )
            await message.channel.send(embed=error_embed)

    # Sub command: /learn <language> <tutorial_name>
    elif len(command_parts) == 3:
        language = command_parts[1].lower()
        tutorial_name = command_parts[2].strip().lower()

        # Check if tutorials exist for the given language
        if language in tutorials:
            # Try to find the tutorial by name
            tutorial = next(
                (t for t in tutorials[language] if t['course_name'].strip().lower() == tutorial_name),
                None
            )

            if tutorial:
                # Create an embed for the specific tutorial
                embed = discord.Embed(
                    title=f'📘 {tutorial["course_name"]}',
                    url=tutorial['url'],
                    description=tutorial['description'],
                    color=discord.Color.green()
                )
                embed.set_author(name=tutorial['site_name'])
                embed.add_field(name='⏳ Course Duration', value=tutorial['duration'], inline=True)
                embed.add_field(name='🗣️ Language', value=tutorial['language'], inline=True)
                embed.add_field(name='👨‍🏫 Instructor', value=tutorial['instructor'], inline=True)
                embed.add_field(name='💵 Type', value=tutorial['type'], inline=True)

                await message.channel.send(embed=embed)
            else:
                # Error: Tutorial not found under the specified language
                not_found_embed = discord.Embed(
                    title='❌ Tutorial Not Found',
                    description=f"Could not find '{tutorial_name}' under {language.capitalize()} tutorials.",
                    color=discord.Color.orange()
                )
                await message.channel.send(embed=not_found_embed)
        else:
            # Error: No tutorials found for the specified language
            error_embed = discord.Embed(
                title='🔍 Language Not Found',
                description=f"Sorry, I don't have any tutorials for '{language}'.",
                color=discord.Color.red()
            )
            await message.channel.send(embed=error_embed)

    # Invalid command format
    else:
        syntax_error = discord.Embed(
            title='❌ Invalid Command Format',
            description='Please use `/learn <language>` to get a list or `/learn <language> <tutorial_name>` for specific details.',
            color=discord.Color.yellow()
        )
        await message.channel.send(embed=syntax_error)
