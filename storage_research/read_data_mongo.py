from util import time_it
from random import randint
from config import config
from statistics import mean
from pprint import pprint
from pymongo import MongoClient
from config import config

MOVIE_RATING_AVG_TIME = []
MOVIE_RATING_COUNT_TIME = []
USER_LIKED_MOVIES_TIME = []

TEST_COUNT = config['test']['read_test_count']
USERS_COUNT = config['test']['users_count']
MOVIES_COUNT = config['test']['movies_count']


@time_it
def avg_rating(collection, movie_id):
    pipline = [
        {
            "$match": {
                "movie_id": movie_id
            }
        },
        {
            "$group": {
                "_id": "$movie_id",
                "AverageValue": {"$avg":"$rating"} }
        }
    ]
    result = collection.aggregate(pipline)
    result.__next__()

@time_it
def all_user_ratings(collection, user_id):
    user = {"user_id": user_id}
    results = collection.find(user)
    list(results)

@time_it
def count_rated_movies(collection, movie_id):
    collection.count_documents({"movie_id": movie_id})
    # return results

def main():
    client = MongoClient(config['mongo']['host'], config['mongo']['port'])
    db = client['someDb']
    series = db['someCollection']
    for test in range(TEST_COUNT):

        id = randint(0, MOVIES_COUNT)
        query_time = avg_rating(series, id)
        MOVIE_RATING_AVG_TIME.append(query_time)

        id = randint(0, MOVIES_COUNT)
        query_time = count_rated_movies(series, id)
        MOVIE_RATING_COUNT_TIME.append(query_time)

        id = randint(0, USERS_COUNT)
        query_time = all_user_ratings(series, id)
        USER_LIKED_MOVIES_TIME.append(query_time)


if __name__ == '__main__':
    main()
    results = ()
    sep = ''.join(['-' for item in range(40)])
    print('TESTS COUNT: ', TEST_COUNT)
    print(sep)
    print('movie avg rating query time stats')
    print('MAX: ', max(MOVIE_RATING_AVG_TIME),
          'MIN: ', min(MOVIE_RATING_AVG_TIME),
          'MEAN: ', round(mean(MOVIE_RATING_AVG_TIME),3))
    print(sep)
    print('movie rating count query time stats')
    print('MAX: ', max(MOVIE_RATING_COUNT_TIME),
          'MIN: ', min(MOVIE_RATING_COUNT_TIME),
          'MEAN: ', round(mean(MOVIE_RATING_COUNT_TIME), 3))
    print(sep)
    print('movie liked by user query time stats')
    print('MAX: ', max(USER_LIKED_MOVIES_TIME),
          'MIN: ', min(USER_LIKED_MOVIES_TIME),
          'MEAN: ', round(mean(USER_LIKED_MOVIES_TIME), 3))
    print(sep)
