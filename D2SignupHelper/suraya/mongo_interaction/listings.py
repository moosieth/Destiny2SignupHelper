import pymongo
import datetime

from bson import ObjectId

from suraya.mongo_interaction.mongo_config import gen_mongo_client


def make_listing(poster_id: int, guild_id: int, activity: str, num_needed: int):
    client = gen_mongo_client()
    db = client.Main
    coll = db.Listings

    post = {
        "leader": poster_id,
        "activity": activity,
        "time": "TODO",
        "needed": num_needed,
        "attendees": [],
        "maybes": [],
    }

    return coll.insert_one(post).inserted_id


def rsvp_to_listing(listing_id: str, user_id: int):
    client = gen_mongo_client()
    db = client.Main
    coll = db.Listings

    query = {"_id": ObjectId(listing_id)}
    updt = {"$push": {"attendees": user_id}}

    return coll.update_one(query, updt)


def rsvp_as_backup(listing_id: str, user_id: int):
    client = gen_mongo_client()
    db = client.Main
    coll = db.Listings

    query = {"_id": ObjectId(listing_id)}
    updt = {"$push": {"maybes": user_id}}

    return coll.update_one(query, updt)
