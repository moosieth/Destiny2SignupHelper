from enum import Enum

import datetime

from bson import ObjectId

from suraya.mongo_interaction.mongo_config import gen_mongo_client


class GuildSettings(Enum):
    TIME = "Time Zone"
    NOTIF = "Notify @everyone on new posting"


def make_guild_entry(guild_id: int):

    client = gen_mongo_client()
    db = client.Main
    coll = db.Guilds

    guild = {
        "guild": guild_id,
        "timezone": "America/New_York",
        "notify_all": False,
    }

    return coll.insert_one(guild).inserted_id


def update_guild_default(setting: GuildSettings, val: str):
    return
