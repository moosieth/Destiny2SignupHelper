import discord
from discord.ext import commands
from discord import app_commands
import os
import logging
import dotenv

from d2signuphelper.mongo_interaction.mongo_config import gen_mongo_client
from d2signuphelper.views.listing_view import (
    RSVPButton,
    BackupButton,
)
from d2signuphelper.assets.activities import Raids, Dungeons, Rituals
from d2signuphelper.mongo_interaction.guilds import (
    make_guild_entry,
    update_guild_default,
)
from d2signuphelper.mongo_interaction.listings import (
    make_listing,
    rsvp_to_listing,
    rsvp_as_backup,
)

logger = logging.getLogger(__name__)

environ = dotenv.dotenv_values(".env")

TOKEN = environ["TOKEN"]
GUILD_ID = int(environ["GUILD_ID"])
OWNER_ID = int(environ["OWNER_ID"])


def bot_init():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="!", intents=intents)

    logging.basicConfig(filename="d2suh.log", level=logging.INFO)

    @bot.event
    async def on_ready():
        logger.info("Bot logged in.")

    @bot.event
    async def on_guild_join(guild):
        insert_result = make_guild_entry(guild.id)

        if guild.system_channel:
            embed = discord.Embed(title="Welcome to Suraya!")
            embed.add_field(
                name="About this bot",
                value="This bot can be used to create and manage LFG postings for Destiny 2.",
                inline=False,
            )
            embed.add_field(
                name="Default behavior",
                value=f"The default settings for this bot are:",
                inline=False,
            )

            await guild.system_channel.send(embed=embed)
        else:
            logger.warn(
                f"Joined guild {str(guild.id)}, but it didn't have a master system channel. We inserted its defaults into Mongo at ID: {str(insert_result)}."
            )

    @bot.command()
    async def sync(ctx):
        if ctx.author.id != OWNER_ID:
            return

        try:
            g = discord.Object(id=GUILD_ID)
            synced = await bot.tree.sync()
            logger.info(f"Tree synced, {len(synced)} commands available.")
            await ctx.send(f"Tree Synced, {len(synced)} commands registered.")
        except Exception as e:
            logger.error(f"Error synching tree: {e}.")
            await ctx.send(f"Tree NOT Synced: {e}.")

    @bot.tree.command(name="ping", description="Ping the bot.")
    async def list(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    """Create a listing for a Raid activity
    """

    @bot.tree.command(name="lfg-raid", description="Create an LFG listing for a raid")
    @app_commands.describe(activity="The raid you're doing")
    @app_commands.choices(
        activity=[
            app_commands.Choice(name=option.value, value=option.value)
            for option in Raids
        ]
    )
    @app_commands.choices(
        needed=[
            app_commands.Choice(name=str(option), value=option)
            for option in range(1, 6)
        ]
    )
    async def lfg_raid(interaction: discord.Interaction, activity: str, needed: int):
        # Create a posting within MongoDB
        mongo_id = make_listing(
            poster_id=interaction.user.id,
            guild_id=interaction.guild.id,
            activity="Raid - " + activity,
            num_needed=needed,
        )

        embed = discord.Embed(title=f"Raid: {activity}")
        embed.set_thumbnail(
            url="https://d1lss44hh2trtw.cloudfront.net/assets/article/2023/02/21/destiny-2-lightfall-raid-release-time_feature.jpg"
        )
        embed.add_field(
            name="Leader", value=f"{interaction.user.mention}", inline=False
        )
        embed.add_field(name="Time", value=f"TODO", inline=False)
        embed.add_field(name="Description", value=f"TODO", inline=False)
        embed.add_field(name="Time", value=f"TODO", inline=False)
        embed.add_field(name="Participants", value=f"", inline=False)
        embed.add_field(name="Backups", value=f"", inline=False)

        # Make view, add RSVP buttons
        view = discord.ui.View(timeout=None)
        view.add_item(
            RSVPButton(
                listing_mongo_id=str(mongo_id),
                max=needed,
                creator=interaction.user.id,
            )
        )
        view.add_item(
            BackupButton(listing_mongo_id=str(mongo_id), creator=interaction.user.id)
        )

        # Send message for posting
        await interaction.response.send_message(
            embed=embed,
            view=view,
        )

    """Create a listing for a Dungeon activity
    """

    @bot.tree.command(
        name="lfg-dungeon", description="Create an LFG listing for a dungeon"
    )
    @app_commands.describe(activity="The dungeon you're doing")
    @app_commands.choices(
        activity=[
            app_commands.Choice(name=option.value, value=option.value)
            for option in Dungeons
        ]
    )
    @app_commands.choices(
        needed=[
            app_commands.Choice(name=str(option), value=option)
            for option in range(1, 3)
        ]
    )
    async def lfg_dungeon(interaction: discord.Interaction, activity: str, needed: int):

        embed = discord.Embed(title=f"Raid: {activity}")
        embed.set_thumbnail(
            url="https://i0.wp.com/kyberscorner.com/wp-content/uploads/2023/02/Destiny-2-Lightfall-Dungeons.jpg?fit=1920%2C1080&ssl=1"
        )
        embed.add_field(
            name="Leader", value=f"{interaction.user.mention}", inline=False
        )
        embed.add_field(name="Time", value=f"TODO", inline=False)
        embed.add_field(name="Description", value=f"TODO", inline=False)
        embed.add_field(name="Time", value=f"TODO", inline=False)
        embed.add_field(name="Participants", value=f"", inline=False)
        embed.add_field(name="Backups", value=f"", inline=False)

        # Make view, add RSVP buttons
        view = discord.ui.View(timeout=None)
        view.add_item(
            RSVPButton(
                listing_mongo_id=str(mongo_id),
                max=needed,
                creator=interaction.user.id,
            )
        )
        view.add_item(
            BackupButton(listing_mongo_id=str(mongo_id), creator=interaction.user.id)
        )

        # Send message for posting
        await interaction.response.send_message(
            embed=embed,
            view=view,
        )

    bot.run(TOKEN)
