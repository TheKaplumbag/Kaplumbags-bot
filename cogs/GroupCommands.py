import os
import requests
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

class GroupCommands(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @app_commands.command(name="grouptest", description="Hi")
  async def groupTest(self, interaction: discord.Interaction):
    await interaction.response.send_message("HI")



async def setup(bot: commands.Bot):
  await bot.add_cog(GroupCommands(bot))