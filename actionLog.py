import discord
from discord.ext import commands
import datetime
import os 
from dotenv import load_dotenv

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL"))


async def send_log(bot, title, description, color: discord.Color = discord.Color.blue(), fields=None):
    """
    Sends a log message to a specific Discord channel.
    
    :param bot: The bot instance.
    :param title: Title of the log embed.
    :param description: Main description/message.
    :param color: Embed color (default blue).
    :param fields: Dictionary of extra fields {name: value}.
    """
    # Replace this with your actual Log Channel ID
    
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if not channel:
        try:
            channel = await bot.fetch_channel(LOG_CHANNEL_ID)
        except:
            print(f"Log Channel with ID {LOG_CHANNEL_ID} not found.")
            return

    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    
    if fields:
        for name, value in fields.items():
            embed.add_field(name=name, value=value, inline=False)
            
    embed.set_footer(text="Action Log System")
    
    await channel.send(embed=embed)
