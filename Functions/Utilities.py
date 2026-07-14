import re
import discord
from discord.ext import commands
import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL"))

async def send_log(bot, title, description, color: discord.Color = discord.Color.blue(), fields=None) -> None:
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


def calculate(duration_str: str) -> str:
  duration_str = duration_str.strip().lower()
  perms =  ["0", "perma", "perm", "0s"]
  if duration_str in perms:
    return None
  else: 
      match = re.match(r"^(\d+)([mhdws]?)$", duration_str)
      if not match:
        return None
        
      value = int(match.group(1))
      unit = match.group(2)
    
    # multipliers
      multipliers = {
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800, 
        "s": 1,
        "": 1 #If empty excepts the time as seconds
        }
    
      exact_seconds = value * multipliers.get(unit, 1)
      return f"{exact_seconds}s"

def FindUserId(username: str) -> int:
  username = username.strip()
  url = "https://users.roblox.com/v1/usernames/users"
  headers = {
    "Content-Type": "application/json"
  }
  Body = {
    "usernames": [
      username
      ],
      "excludeBannedUsers": True
  }
  try:
    response = requests.post(url, headers=headers, json=Body)
    if response.status_code == 200:
      data = response.json()
      if "data" not in data or not data["data"]:
        return "NO DATA HAS BEEN FOUND"
      else:
        return data["data"][0]["id"]
    else:
      print(f"AN ERROR HAS BEEN ACCOURED! {response.status_code}: {response.text} ")
  except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


# HI IF YOU SEE THIS UR KINDA TUFF