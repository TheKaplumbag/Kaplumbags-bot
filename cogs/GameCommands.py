import discord
import logging
import os 
import json
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from Functions.Utilities import send_log,calculate,FindUserId
import requests
from Functions.GameFunctions import UserGameBan, GetGameBanHistory,UnGameBan,GetPlayerHistory
import asyncio

load_dotenv()

API_KEY = os.getenv("API_KEY")
UNIVERSE_ID = os.getenv("UNIVERSE_ID")
PLACE_ID = os.getenv("PLACE_ID")



class GameCommands(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  
  
  @app_commands.command(name="gameban", description="To set durations use h,d,w,m, perm, 0s for permban if no unit then it will be second")
  #@discord.app_commands.checks.has_any_role("Game Moderator","Admin", "Head Admin", "Creator")
  @discord.app_commands.checks.has_role(1384526591173853316)
  @app_commands.checks.cooldown(1, 25.0, key=lambda i: i.user.id)
  async def Gameban(self, interaction: discord.Interaction,
  player: str, 
  duration: str, 
  display_reason: str,
  private_reason: str = "No private reason provided!", 
  ban_alts: bool = False):
    await interaction.response.defer(thinking=True)
    userId = FindUserId(player)
    calcedDur = calculate(duration)
    success, status = UserGameBan(userId, duration, display_reason, private_reason, ban_alts)
    if success:
      await send_log(self.bot,"User has been banned from the game!",f"Moderator: {interaction.user.mention}\nOffender: {player.strip()}\nUserID: {userId}\nDuration: {duration}({calcedDur})\nDisplay reason: {display_reason}\nPrivate reason: {private_reason}\nAlts included?: {ban_alts}", discord.Color.red())
      await interaction.followup.send(status)
    else:
      await interaction.followup.send(status)
  @Gameban.error
  async def ban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    try:
      if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"Slow down! Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
      elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
      else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
    except discord.HTTPException as e:
            print(f"Network error while handling command error: {e}")
  """
  @app_commands.command(name="get-banlogs", description= "Get full banlogs of people qho got banned via ban api.")
  # @discord.app_commands.checks.has_any_role("Game Moderator","Admin", "Head Admin", "Creator")
  # Test server role id
  @discord.app_commands.checks.has_role(1384526591173853316)
  @app_commands.checks.cooldown(2, 60.0, key=lambda i: i.user.id)
  async def FullBanLogs(self, interaction: discord.Interaction):
    List = GetGameBanHistory()
    await interaction.response.send_message(List)
  """
  @app_commands.command(name="ungameban", description="Unban someone from game")
  #@discord.app_commands.checks.has_any_role("Game Moderator","Admin", "Head Admin", "Creator")
  @discord.app_commands.checks.has_role(1384526591173853316)
  @app_commands.checks.cooldown(1, 25.0, key=lambda i: i.user.id)
  async def UnGameban(self, interaction: discord.Interaction,
  player: str,
  display_reason: str,
  private_reason: str = "No private reason provided!"):
    await interaction.response.defer(thinking=True)
    userId = FindUserId(player)
    success, status = UnGameBan(userId, display_reason, private_reason)
    if success:
      await send_log(self.bot,"User has been unbanned from the game!",f"Moderator: {interaction.user.mention}\nOffender: {player.strip()}\nUserID: {userId}\nDisplay reason: {display_reason}\nPrivate reason: {private_reason}", discord.Color.red())
      await interaction.followup.send(status)
    else:
      await interaction.followup.send(status)
  @UnGameban.error
  async def unban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    try:
      if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"Slow down! Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
      elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
      else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
    except discord.HTTPException as e:
            print(f"Network error while handling command error: {e}")
  
  
  
  
async def setup(bot: commands.Bot):
  await bot.add_cog(GameCommands(bot))