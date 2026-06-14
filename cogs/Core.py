import discord
import logging
import os 
import json
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from actionLog import send_log
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
UNIVERSE_ID = os.getenv("UNIVERSE_ID")
PLACE_ID = os.getenv("PLACE_ID")


def GetFullBanList():
  url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/user-restrictions:listLogs"
  headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
  }
  
  response = requests.get(url, headers=headers)
  
  if response.status_code == 200:
    data = json.loads(response.text)
    
    if "logs" not in data or not data["logs"]:
      return "📋 **Ban Logs:** No active bans found."
    
    formatted_message = "📋 **ROBLOX BAN LOGS**\n\n"
    
    for log in data["logs"]:
      user_id = log["user"].split("/")[-1]
      mod_id = log["moderator"]["robloxUser"].split("/")[-1]
      
      user_link = f"https://www.roblox.com/users/{user_id}/profile"
      mod_link = f"https://www.roblox.com/users/{mod_id}/profile"
      
      public_reason = log.get("displayReason", "No reason provided")
      private_reason = log.get("privateReason", "No internal reason")
      
      formatted_message += f"👤 **User:** [Profile Link]({user_link}) *(ID: {user_id})*\n"
      formatted_message += f"🛠️ **Moderator:** [Profile Link]({mod_link})\n"
      formatted_message += f"📄 **Reason:** {public_reason}\n"
      formatted_message += f"🔒 **Internal Note:** *{private_reason}*\n"
      formatted_message += "---------------------------------------\n"
        
    return formatted_message

  else:
    print(f"API Error {response.status_code}: {response.text}")
    return f"⚠️ API Error: {response.status_code}"




class Core(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  """
  @app_commands.command(name="perma-gameban", description="Bans a roblox user from the game.")
  @app_commands.checks.cooldown(1, 25.0, key=lambda i: i.user.id)
  async def Perma_Gameban(self, interaction: discord.Interaction, player: str, display-reason: str = "You've been banned from the game by an Admin. You can apply from our discord server (DM thekaplumbag.)", private-reason: str = "No private reason provided!", alts-included: bool):
    try:
      continue
  @Perma_Gameban.error
  async def ban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
      await interaction.response.send_message(f"Slow down! Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
    elif isinstance(error, app_commands.MissingPermissions):
      await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    else:
      await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
  """
  
  @app_commands.command(name="get-banlogs", description= "Get full banlogs of people qho got banned via ban api.")
  # @discord.app_commands.checks.has_any_role("Game Moderator","Admin", "Head Admin", "Creator")
  # Test server role id
  @discord.app_commands.checks.has_role(1384526591173853316)
  @app_commands.checks.cooldown(2, 60.0, key=lambda i: i.user.id)
  async def FullBanLogs(self, interaction: discord.Interaction):
    List = GetFullBanList()
    await interaction.response.send_message(List)
    


async def setup(bot: commands.Bot):
  await bot.add_cog(Core(bot))