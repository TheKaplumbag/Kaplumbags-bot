# IMPORTING REQUIREMENTS
import discord
import logging
from dotenv import load_dotenv
import os
from discord import app_commands
import asyncio
from discord.ext import commands 

load_dotenv()
TOKEN = os.getenv("TOKEN")
DEV_GUILD = os.getenv("DEV_GUILD")

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
    
if __name__=="__main__":
  if not TOKEN:
    raise SystemExit("NO TOKEN FOUND INSIDE .env!")

  bot = Bot()
  bot.run(TOKEN)