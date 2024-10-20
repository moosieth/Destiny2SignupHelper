import pymongo
import os


def gen_mongo_client():
    uri = os.environ.get('MONGO_URI')

    client = pymongo.MongoClient(uri)

    return client
