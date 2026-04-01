import discord
import asyncio

# --- CONFIGURATION ---
TARGET_ID = 1467281888212422841  # Replace with the bot/user ID
BOT_TOKEN = 'MTQ4ODcwMTIwODc4NDAxMTMyNA.G7z-3J.sx_wP6o9CUNdnvvHfvm8UsSTzkd7Zhio3rYGkE'
# ---------------------

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Success! Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore the bot's own messages
    if message.author == client.user:
        return

    # 1. AUTO-DELETE NEW MESSAGES
    if message.author.id == TARGET_ID:
        try:
            await message.delete()
            print(f"Auto-deleted new message from target in #{message.channel}")
        except discord.HTTPException:
            pass

    # 2. THE PURGE COMMAND (Only Admins can use this)
    if message.content == '!wipetarget' and message.author.guild_permissions.administrator:
        await message.channel.send("Scanning and deleting target's messages... this might take a minute due to Discord rate limits.")
        
        # A simple check function so the bot only deletes the target's messages
        def is_target(m):
            return m.author.id == TARGET_ID

        try:
            # Purge scans up to 1000 messages back in the channel. 
            # It will automatically handle the 14-day rule and rate limits.
            deleted = await message.channel.purge(limit=1000, check=is_target)
            
            confirmation = await message.channel.send(f"Done! Deleted {len(deleted)} messages from the target in this channel.")
            
            # Clean up the confirmation message after 5 seconds
            await asyncio.sleep(5)
            await confirmation.delete()
            await message.delete() # Delete the original '!wipetarget' command

        except discord.Forbidden:
            await message.channel.send("Error: I need the 'Manage Messages' and 'Read Message History' permissions!")
        except discord.HTTPException as e:
            await message.channel.send(f"Hit an API error: {e}")

client.run(BOT_TOKEN)