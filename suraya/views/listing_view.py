import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View

import re

from suraya.assets.activities import ActivityType
from suraya.mongo_interaction.listings import (
    make_listing,
    rsvp_to_listing,
    rsvp_as_backup,
)


class RSVPButton(Button):
    def __init__(self, listing_mongo_id: str, max: int, creator: int):
        self.mongo_id = listing_mongo_id
        self.max = max
        self.cur = 0
        self.creator = creator
        super().__init__(
            label="Count me in!",
            style=discord.ButtonStyle.grey,
            emoji="\N{THUMBS UP SIGN}",
        )

    async def callback(self, interaction: discord.Interaction):
        if self.creator == interaction.user.id:
            await interaction.response.send_message(
                "You can't RSVP to your own listing - you're already in it, silly!",
                ephemeral=True,
            )
            return

        embed = interaction.message.embeds[0]
        if interaction.user.mention in embed.fields[3].value:
            await interaction.response.send_message(
                "You are already a participant for that listing!",
                ephemeral=True,
            )
            return

        insert_result = rsvp_to_listing(
            listing_id=self.mongo_id, user_id=interaction.user.id
        )

        if insert_result.modified_count == 1:
            self.cur += 1

        # Update embed
        participants = (
            embed.fields[3].value
            + f"""{interaction.user.mention}
        {chr(173)}"""
        )
        embed.set_field_at(3, name="Participants", value=participants, inline=False)

        if self.cur >= self.max:
            self.view.remove_item(self)

        await interaction.response.edit_message(embed=embed, view=self.view)


class BackupButton(Button):
    def __init__(self, listing_mongo_id: str, creator: int):
        self.mongo_id = listing_mongo_id
        self.creator = creator
        super().__init__(
            label="I'll be a Backup",
            style=discord.ButtonStyle.grey,
            emoji="\N{WARNING SIGN}",
        )

    async def callback(self, interaction: discord.Interaction):
        if self.creator == interaction.user.id:
            await interaction.response.send_message(
                "You can't RSVP to your own listing - you're already in it, silly!",
                ephemeral=True,
            )
            return

        embed = interaction.message.embeds[0]
        if interaction.user.mention in embed.fields[4].value:
            await interaction.response.send_message(
                "You are already a backup for that listing!",
                ephemeral=True,
            )
            return

        insert_result = rsvp_as_backup(
            listing_id=self.mongo_id, user_id=interaction.user.id
        )

        # Update embed
        backups = (
            embed.fields[4].value
            + f"""{interaction.user.mention}
        {chr(173)}"""
        )
        embed.set_field_at(4, name="Backups", value=backups, inline=False)

        await interaction.response.edit_message(embed=embed, view=self.view)
