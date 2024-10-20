import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View

import re

from d2signuphelper.assets.activities import ActivityType
from d2signuphelper.mongo_interaction.listings import (
    make_listing,
    rsvp_to_listing,
    rsvp_as_backup,
)


class RSVPButton(
    discord.ui.DynamicItem[discord.ui.Button],
    template=r"rsvp:user:(?P<id>[0-9]+):mongoid:(?P<mid>[a-fA-F0-9]+):max:(?P<max>[0-9]+):cur:(?P<cur>[0-9]+)",
):
    def __init__(
        self, user_id: int, listing_mongo_id: str, max: int, cur: int = 0
    ) -> None:
        self.user_id: int = user_id
        self.max: int = max
        self.cur = cur
        self.mongo_id = listing_mongo_id
        super().__init__(
            discord.ui.Button(
                label="Count me in!",
                style=self.style,
                custom_id=f"rsvp:user:{user_id}:mongoid:{listing_mongo_id}:max:{max}:cur:{cur}",
                emoji="\N{THUMBS UP SIGN}",
            )
        )

    @property
    def style(self) -> discord.ButtonStyle:
        if self.cur < self.max:
            return discord.ButtonStyle.grey
        self.disabled = True
        return discord.ButtonStyle.red

    # This method actually extracts the information from the custom ID and creates the item.
    @classmethod
    async def from_custom_id(
        cls,
        interaction: discord.Interaction,
        item: discord.ui.Button,
        match: re.Match[str],
        /,
    ):
        mongo_id = str(match["mid"])
        user_id = int(match["id"])
        max = int(match["max"])
        cur = int(match["cur"])
        return cls(user_id, listing_mongo_id=mongo_id, max=max, cur=cur)

    # We want to ensure that our button is only called by the user who created it.
    # TODO: Invert this so that the person that made it CANNOT click it
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.cur >= self.max:
            return

        insert_result = rsvp_to_listing(
            listing_id=self.mongo_id, user_id=interaction.user.id
        )

        if insert_result.modified_count == 1:
            self.cur += 1

        # Set button style and ID
        self.item.style = self.style
        self.custom_id = f"rsvp:user:{self.user_id}:mongoid:{self.mongo_id}:max:{self.max}:cur:{self.cur}"

        # Update embed
        embed = interaction.message.embeds[0]
        participants = embed.fields[3].value + f"{interaction.user.mention}\n"
        embed.set_field_at(3, name="Participants", value=participants, inline=False)

        await interaction.response.edit_message(embed=embed, view=self.view)


class BackupButton(
    discord.ui.DynamicItem[discord.ui.Button], template=r"backup:user:(?P<id>[0-9]+)"
):
    def __init__(self, user_id: int, listing_mongo_id: str) -> None:
        self.user_id: int = user_id
        self.mongo_id = listing_mongo_id
        super().__init__(
            discord.ui.Button(
                label="I'll be a backup!",
                style=self.style,
                custom_id=f"backup:user:{user_id}",
                emoji="\N{WARNING SIGN}",
            )
        )

    @property
    def style(self) -> discord.ButtonStyle:
        return discord.ButtonStyle.grey

    # This method actually extracts the information from the custom ID and creates the item.
    # @classmethod
    # async def from_custom_id(cls, interaction: discord.Interaction, item: discord.ui.Button, match: re.Match[str], /):
    #     count = int(match['count'])
    #     user_id = int(match['id'])
    #     return cls(user_id, count=count)

    async def callback(self, interaction: discord.Interaction) -> None:
        insert_result = rsvp_as_backup(
            listing_id=self.mongo_id, user_id=interaction.user.id
        )

        if insert_result.modified_count == 1:
            self.item.style = discord.ButtonStyle.green
