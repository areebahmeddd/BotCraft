import discord

# Function to collect user input
async def get_user_input(message, user_id, prompt, field_name, bot):
    # Send prompt and wait for user response
    await message.channel.send(prompt)
    
    # Create a check function to only accept responses from the correct user in the right channel
    def check(m):
        return m.author.id == user_id and m.channel == message.channel
    
    response = await bot.wait_for("message", check=check)
    
    return response.content
