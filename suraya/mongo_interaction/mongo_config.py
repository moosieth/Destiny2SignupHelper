import pymongo
import os
import dotenv

environ = dotenv.dotenv_values(".env")
MONGO_URI = environ["MONGO_URI"]


def gen_mongo_client():
    return pymongo.MongoClient(MONGO_URI)
