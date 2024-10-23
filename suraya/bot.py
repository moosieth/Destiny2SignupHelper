import discord
from discord.ext import commands
from discord import app_commands
import os
import logging
import dotenv

from suraya.mongo_interaction.mongo_config import gen_mongo_client
from suraya.views.listing_view import (
    RSVPButton,
    BackupButton,
)
from suraya.assets.activities import Raids, Dungeons, Rituals
from suraya.mongo_interaction.guilds import (
    make_guild_entry,
    update_guild_default,
)
from suraya.mongo_interaction.listings import (
    make_listing,
)

logger = logging.getLogger(__name__)

environ = dotenv.dotenv_values(".env")

TOKEN = environ["TOKEN"]
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
                value="Suraya is an open-source Discord bot that creates and manages LFG postings for Destiny 2.",
                inline=False,
            )
            embed.add_field(
                name="What's new?",
                value=f"You can read the Changelog for Suraya [here](TODO - Insert Changelog Link here).",
                inline=False,
            )
            embed.add_field(
                name="Getting started",
                value=f"To display the details of all of Suraya's commands, use the `/help` command. To jump right in, try `/lfg-raid` or `/lfg-dungeon`!",
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
            synced = await bot.tree.sync()
            logger.info(f"Tree synced, {len(synced)} commands available.")
            await ctx.send(f"Tree Synced, {len(synced)} commands registered.")
        except Exception as e:
            logger.error(f"Error synching tree: {e}.")
            await ctx.send(f"Tree NOT Synced: {e}.")

    @bot.tree.command(name="ping", description="Ping the bot.")
    async def list(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @bot.tree.command(name="help", description="Display a help message that outlines all of Suraya's commands")
    async def list(interaction: discord.Interaction):
        await interaction.response.send_message("TODO")

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
    @app_commands.describe(needed="The number of players you're looking to recruit")
    @app_commands.choices(
        needed=[
            app_commands.Choice(name=str(option), value=option)
            for option in range(1, 6)
        ]
    )
    @app_commands.describe(description="Any info you think potential participants should know")
    @app_commands.describe(time="Time you want to start the activity. Of the form: `HH:MM{a|p}`")
    async def lfg_raid(interaction: discord.Interaction, activity: str, needed: int, description: str, time: str):
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
        embed.add_field(name="Description", value=description, inline=False)
        embed.add_field(name="Time", value=time, inline=False)
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
    @app_commands.describe(needed="The number of players you're looking to recruit")
    @app_commands.choices(
        needed=[
            app_commands.Choice(name=str(option), value=option)
            for option in range(1, 3)
        ]
    )
    @app_commands.describe(description="Any info you think potential participants should know")
    @app_commands.describe(time="Time you want to start the activity. Of the form: `HH:MM{a|p}`")
    async def lfg_dungeon(interaction: discord.Interaction, activity: str, needed: int, description: str, time: str):
        # Create a posting within MongoDB
        mongo_id = make_listing(
            poster_id=interaction.user.id,
            guild_id=interaction.guild.id,
            activity="Raid - " + activity,
            num_needed=needed,
        )
        
        embed = discord.Embed(title=f"Raid: {activity}")
        embed.set_thumbnail(
            url="https://i0.wp.com/kyberscorner.com/wp-content/uploads/2023/02/Destiny-2-Lightfall-Dungeons.jpg?fit=1920%2C1080&ssl=1"
        )
        embed.add_field(
            name="Leader", value=f"{interaction.user.mention}", inline=False
        )
        embed.add_field(name="Time", value=time, inline=False)
        embed.add_field(name="Description", value=description, inline=False)
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
