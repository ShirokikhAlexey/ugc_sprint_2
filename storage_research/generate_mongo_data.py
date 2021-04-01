from pymongo import MongoClient
from util import generate_movie_rating_mongo
from config import config

client = MongoClient(config['mongo']['host'], config['mongo']['port'])
USERS_COUNT = config['test']['users_count']
MOVIES_COUNT = config['test']['movies_count']
db = client['someDb']
series = db['someCollection']

def insert_many(collection, data):
    return collection.insert_many(data).inserted_ids

data = generate_movie_rating_mongo(USERS_COUNT, MOVIES_COUNT)
result = insert_many(series, data)
