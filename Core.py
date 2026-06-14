import discord
import logging
from discord import app_commands
from discord.ext import commands
from actionLog import send_log

class Core(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @app_commands.command(name="ban", description="Ban a member from the server")
  @app_commands.checks.has_permissions(ban_members=True)
  @app_commands.checks.cooldown(1, 25.0, key=lambda i: i.user.id)
  async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
      await member.ban(reason=reason)
      await interaction.response.send_message(f"Successfully banned {member.mention} for: {reason}")
      await send_log(self.bot, "BAN LOG", f"{interaction.user.mention} banned {member.name} for {reason}", discord.Color.red())
    except discord.Forbidden:
      await interaction.response.send_message("I don't have permission to ban this member.", ephemeral=True)
    except Exception as e:
      await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
  @ban.error
  async def ban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
      await interaction.response.send_message(f"Slow down! Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
    elif isinstance(error, app_commands.MissingPermissions):
      await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    else:
      await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)


async def setup(bot: commands.Bot):
  await bot.add_cog(Core(bot))