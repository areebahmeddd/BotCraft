import discord
import asyncio

# User data storage
user_data = {}

# Items available for purchase
items = {
    'enchanted_sword': {'xp_cost': 10, 'damage': 10, 'emoji': '⚔️'},
    'magical_axe': {'xp_cost': 20, 'damage': 20, 'emoji': '🪓'},
    'legendary_blaster': {'xp_cost': 50, 'damage': 50, 'emoji': '🔫'},
}

# Roles based on user levels
roles = {
    2: 'Novice Adventurer',
    10: 'Seasoned Explorer',
    50: 'Master Warrior',
    100: 'Legendary Hero',
}

async def focus_commands(message, bot):
    command_parts = message.content.split()

    # Check if a subcommand is provided
    if len(command_parts) < 2:
        await message.channel.send("Please provide a subcommand (e.g., `/focus pomodoro`, `/focus buy`).")
        return

    subcommand = command_parts[1]

    # Sub command: /focus pomodoro <minutes>
    if subcommand == 'pomodoro':
        await pomodoro_command(message)
    # Sub command: /focus level
    elif subcommand == 'level':
        await level_command(message)
    # Sub command: /focus xp
    elif subcommand == 'xp':
        await xp_command(message)
    # Sub command: /focus inventory
    elif subcommand == 'inventory':
        await inventory_command(message)
    # Sub command: /focus buy
    elif subcommand == 'buy':
        await buy_command(message, bot)
    # Sub command: /focus fight
    elif subcommand == 'fight':
        await fight_command(message)
    else:
        await message.channel.send("Invalid subcommand. Use `/focus pomodoro`, `/focus level`, `/focus xp`, `/focus inventory`, `/focus buy`, or `/focus fight`.")

async def pomodoro_command(message):
    # Get the duration for the Pomodoro session
    minutes = int(message.content.split()[2])
    xp_per_minute = 20
    total_xp = minutes * xp_per_minute

    countdown_message = await message.channel.send(f"Pomodoro started for {minutes} minutes! Counting down...")
    total_seconds = minutes * 60

    # Countdown logic
    while total_seconds > 0:
        mins, secs = divmod(total_seconds, 60)
        timer_display = f"{mins:02d}:{secs:02d}"
        await countdown_message.edit(content=f"Time remaining: {timer_display}")
        await asyncio.sleep(1)
        total_seconds -= 1

    await countdown_message.edit(content=f"Time's up, {message.author.mention}! You've completed a Pomodoro session!")

    # Update XP after Pomodoro session
    user_id = message.author.id
    user_xp = user_data.get(user_id, {'xp': 0, 'level': 1, 'inventory': []})
    user_xp['xp'] += total_xp

    # Check if user levels up and assign role
    while True:
        level_up_xp = 10 * (2 ** (user_xp['level'] - 1))
        if user_xp['xp'] >= level_up_xp:
            user_xp['level'] += 1
            user_xp['xp'] -= level_up_xp
            await assign_role(message.author, user_xp['level'], message.guild)
            await message.channel.send(f"🎉 {message.author.mention} leveled up to level {user_xp['level']}!")
        else:
            break

    user_data[user_id] = user_xp
    await message.channel.send(f"{message.author.mention}, you've earned {total_xp} XP! Your total XP is now {user_xp['xp']} at level {user_xp['level']}.")

async def level_command(message):
    # Get the user's current level and role
    user_id = message.author.id
    user_xp = user_data.get(user_id, {'xp': 0, 'level': 1, 'inventory': []})
    role_name = None
    for level, role in sorted(roles.items(), reverse=True):
        if user_xp['level'] >= level:
            role_name = role
            break

    await message.channel.send(f"{message.author.mention}, you are at level {user_xp['level']} with the role **{role_name}** and {user_xp['xp']} XP.")

async def xp_command(message):
    # Display the user's current XP and level
    user_id = message.author.id
    user_xp = user_data.get(user_id, {'xp': 0, 'level': 1, 'inventory': []})
    await message.channel.send(f"{message.author.mention}, your current XP is {user_xp['xp']} at level {user_xp['level']}.")

async def inventory_command(message):
    # Display the user's inventory items
    user_id = message.author.id
    user_xp = user_data.get(user_id, {'xp': 0, 'level': 1, 'inventory': []})
    inventory = ', '.join([items[item]['emoji'] + ' ' + item.replace('_', ' ') for item in user_xp['inventory']]) if user_xp['inventory'] else "You have no items in your inventory."
    await message.channel.send(f"{message.author.mention}, your inventory: {inventory}")

async def buy_command(message, bot):
    # Show the items available for purchase
    inventory_message = 'Here are the items you can buy:\n'
    for item_name, item in items.items():
        inventory_message += f"{item['emoji']} {item_name.replace('_', ' ').capitalize()} - {item['xp_cost']} XP\n"
    inventory_message += '\nReact with the emoji of the item you want to purchase!'

    inventory_msg = await message.channel.send(inventory_message)
    for item in items.values():
        await inventory_msg.add_reaction(item['emoji'])

    # Wait for the user to react with an emoji
    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in [item['emoji'] for item in items.values()]

    reaction, _ = await bot.wait_for('reaction_add', check=check)

    selected_item_name = None
    for item_name, item in items.items():
        if item['emoji'] == str(reaction.emoji):
            selected_item_name = item_name
            break

    # Handle item purchase
    if selected_item_name:
        user_id = message.author.id
        user_xp = user_data.get(user_id, {'xp': 0, 'level': 1, 'inventory': []})

        item = items[selected_item_name]
        if user_xp['xp'] >= item['xp_cost']:
            user_xp['xp'] -= item['xp_cost']
            user_xp['inventory'].append(selected_item_name)
            await message.channel.send(f"{message.author.mention} bought a {item['emoji']} {selected_item_name.replace('_', ' ').capitalize()}! Remaining XP: {user_xp['xp']}")
        else:
            await message.channel.send(f"{message.author.mention}, you don't have enough XP to buy a {selected_item_name.replace('_', ' ').capitalize()}.")

        user_data[user_id] = user_xp
    else:
        await message.channel.send("Invalid selection. Please try again.")

async def fight_command(message):
    # Handle fight scenario with a dragon
    user_id = message.author.id
    user_xp = user_data.get(user_id, {'xp': 0, 'level': 1, 'inventory': []})
    await message.channel.send(f"{message.author.mention} is fighting a dragon! Prepare for battle!")

    # Check if the user has a weapon in their inventory
    if 'enchanted_sword' in user_xp['inventory']:
        user_xp['xp'] += items['enchanted_sword']['xp_cost']
        await message.channel.send(f"You used the enchanted sword! You earned {items['enchanted_sword']['xp_cost']} XP!")
    else:
        await message.channel.send(f"You don't have a weapon to fight the dragon. Defeat one to earn a weapon!")
    
    user_data[user_id] = user_xp

async def assign_role(user, level, guild):
    # Assign the appropriate role based on the user's level
    role_name = None
    for level_threshold, role in sorted(roles.items(), reverse=True):
        if level >= level_threshold:
            role_name = role
            break

    if role_name:
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            await user.add_roles(role)
            await user.send(f"You've been assigned the role **{role_name}**!")
