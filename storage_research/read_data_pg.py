import psycopg2
from util import time_it
from random import randint
from config import config
from statistics import mean
from pprint import pprint

MOVIE_RATING_AVG_TIME = []
MOVIE_RATING_COUNT_TIME = []
USER_LIKED_MOVIES_TIME = []

MOVIE_RATING_AVG = "select avg(rating) from public.movie_rating where movie_id = %s;"
MOVIE_RATING_COUNT = "select count(*) from public.movie_rating where movie_id = %s;"
USER_LIKED_MOVIES = "select * from public.movie_rating where user_id = %s;"

queries = (MOVIE_RATING_AVG, MOVIE_RATING_COUNT, USER_LIKED_MOVIES)

TEST_COUNT = config['test']['read_test_count']
USERS_COUNT = config['test']['users_count']
MOVIES_COUNT = config['test']['movies_count']

@time_it
def execute_query(cursor, query: str, id: int):
    cursor.execute(query, (id, ))
    result = cursor.fetchall()


def main():
    conn = psycopg2.connect(**config["pg_dsn"])
    with conn.cursor() as cur:
        for test in range(TEST_COUNT):

            id = randint(0, MOVIES_COUNT)
            query_time = execute_query(cur, MOVIE_RATING_AVG, id)
            MOVIE_RATING_AVG_TIME.append(query_time)

            id = randint(0, MOVIES_COUNT)
            query_time = execute_query(cur, MOVIE_RATING_COUNT, id)
            MOVIE_RATING_COUNT_TIME.append(query_time)

            id = randint(0, USERS_COUNT)
            query_time = execute_query(cur, USER_LIKED_MOVIES, id)
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
