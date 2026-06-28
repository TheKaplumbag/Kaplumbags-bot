# IMPORTING REQUIREMENTS
import discord
import logging
from dotenv import load_dotenv
import os
from discord import app_commands
import asyncio
import aiohttp
from discord.ext import commands 

load_dotenv()
COOKIE = os.getenv("COOKIE")
TOKEN = os.getenv("TOKEN")
DEV_GUILD = os.getenv("DEV_GUILD")

ROBLOSECURITY_COOKIE = COOKIE
roblox_session = None
csrf_token = None

async def refresh_csrf_token():
  global csrf_token, roblox_session
  url = "https://auth.roblox.com/v1/logout"
  
  if roblox_session is None:
    return False
      
  async with roblox_session.post(url) as response:
    token = response.headers.get("x-csrf-token")
    if token:
      csrf_token = token
      roblox_session._default_headers.update({"X-CSRF-TOKEN": csrf_token})
      return True
    return False


class Bot(commands.Bot):
  def __init__(self):
    Intents = discord.Intents.all()
    Intents.guilds = True
    super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=Intents)
    help_command=None
    activity=discord.Game(name="Free Animate [BETA]")

  async def setup_hook(self):
    await self.load_extension("cogs.Core")
    
    if DEV_GUILD and DEV_GUILD.isdigit():
      guild = discord.Object(id=int(DEV_GUILD))
      self.tree.copy_global_to(guild=guild)
      await self.tree.sync(guild=guild)
      
      logging.info(f"Synced commands to DEV_GUILD={DEV_GUILD}")
    else:
       await self.tree.sync()
       logging.info("Synced global commands")

  async def on_ready(self):
    logging.basicConfig(level=logging.INFO)
    logging.info("Logged in as Bot")
    
    global roblox_session
    print(f"Logged into Discord as {self.user}")
    
    if roblox_session is None:
      roblox_session = aiohttp.ClientSession()
        
    roblox_session.cookie_jar.update_cookies({".ROBLOSECURITY": ROBLOSECURITY_COOKIE})
    
    await refresh_csrf_token()
    print("Roblox session initialized.")





    
if __name__=="__main__":
  if not TOKEN:
    raise SystemExit("NO TOKEN FOUND INSIDE .env!")

  bot = Bot()
  bot.run(TOKEN)