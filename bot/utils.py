async def get_user_input(message, user_id, prompt, bot):
    # Send prompt to the user
    await message.channel.send(prompt)
    
    # Wait for a valid response from the correct user in the correct channel
    def check(text):
        return text.author.id == user_id and text.channel == message.channel
    
    response = await bot.wait_for('message', check=check)
    
    return response.content
