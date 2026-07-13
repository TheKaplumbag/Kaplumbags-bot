import os
import requests
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

from Functions.GroupFunctions import groupRoles,groupBan,groupBans,groupUnban

load_dotenv()
GROUP_API : str = os.getenv("GROUP_API_KEY")

class GroupCommands(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @app_commands.command(name="group-roles", description="see group roles [THIS IS A TEST COMMAND THIS MEAN THIS COMMAND WILL BE REMOVED]")
  async def groupRoles(self, interaction: discord.Interaction):
    print("hi")
    await interaction.response.send_message("hi")



async def setup(bot: commands.Bot):
  await bot.add_cog(GroupCommands(bot))