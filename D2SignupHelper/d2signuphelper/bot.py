import discord
from discord.ext import commands
from discord import app_commands
import os
import logging

logger = logging.getLogger(__name__)

# tokenFile = open(os.environ.get('TOKEN'), 'r')
# TOKEN = tokenFile.readline()

TOKEN = 'MTI0NTUzMjg1MDM1MTExMjI1Mg.Gy6lr5.ZixLjfa43BXCWRF69dnJ2vXEk4pbE76GVVfubM'
GUILD_ID = 759853907957514250

def bot_init():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="!",intents=intents)

    logging.basicConfig(filename='d2suh.log', level=logging.INFO)

    @bot.event
    async def on_ready():
        logger.info("Bot logged in.")
    
    @bot.command()
    async def sync(ctx):
        try:
            g = discord.Object(id=GUILD_ID)
            synced = await bot.tree.sync()
            logger.info(f"Tree synced, {len(synced)} commands available.")
            await ctx.send(f"Tree Synced, {len(synced)} commands registered.")
        except Exception as e:
            logger.error(f"Error synching tree: {e}.")
            await ctx.send(f"Tree NOT Synced: {e}.")
        

    @bot.tree.command(name="list", description="Make a list")
    async def list(interaction: discord.Interaction):
        await interaction.response.send_message("Making a list")

    bot.run(TOKEN)
