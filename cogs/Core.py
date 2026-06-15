import discord
import logging
import os 
import json
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from actionLog import send_log
import requests
from Functions import FindUserId,UserGameBan, GetFullBanList
from timeCalc import calc

load_dotenv()

API_KEY = os.getenv("API_KEY")
UNIVERSE_ID = os.getenv("UNIVERSE_ID")
PLACE_ID = os.getenv("PLACE_ID")



class Core(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  
  
  @app_commands.command(name="gameban", description="Bans a roblox user from the game. For durations use s, h, d, w, m put perm, perma, 0, 0s for permban")
  @discord.app_commands.checks.has_any_role("Game Moderator","Admin", "Head Admin", "Creator")
  @app_commands.checks.cooldown(1, 25.0, key=lambda i: i.user.id)
  async def Gameban(self, interaction: discord.Interaction, player: str, duration: str display-reason: str = "You've been banned from the game by an Admin. You can apply from our discord server (DM thekaplumbag.)", private-reason: str = "No private reason provided!", ban-alts: bool = False):
    userId = FindUserId(player)
    calcedDur = calc(duration)
    success, status = UserGameBan(userId, calcedDur, display-reason, private-reason, ban-alts)
    if success:
      await send_log(self.bot,"User has been banned from the game!",f"Moderator: {interaction.user.mention}\nOffender: {player.strip()}\nDisplay reason: {display-reason}\nPrivate reason: {private-reason}\nAlts included?: {ban-alts}", discord.Color.red())
      await interaction.response.send_message(status)
    else:
      await interaction.response.send_message(status)
  @Gameban.error
  async def ban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
      await interaction.response.send_message(f"Slow down! Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
    elif isinstance(error, app_commands.MissingPermissions):
      await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    else:
      await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
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