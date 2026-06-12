import discord
import logging
from discord import app_commands
from discord.ext import commands

class Core(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @app_commands.command(name="ban", description="ban an user")
  async def ban(self, 
  interaction:discord.Interaction, 
  user: discord.User,
  reason: str):
    await interaction.response.send_message(f"{user} has been banned! for {reason}")
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Core(bot))