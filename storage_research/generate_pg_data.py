import psycopg2
from util import generate_movie_user, generate_movie_rating
from random import randint
from psycopg2.extras import execute_batch
from config import config

conn = psycopg2.connect(**config["pg_dsn"])

INSERT_MOVIES_RATING = "INSERT INTO movie_rating VALUES(%s, %s, %s)"
USERS_COUNT = config['test']['users_count']
MOVIES_COUNT = config['test']['movies_count']
INSERT_BATCH_SIZE = config['insert_batch_size']

with conn.cursor() as cur:
    data = generate_movie_rating(USERS_COUNT, MOVIES_COUNT)
    execute_batch(cur, INSERT_MOVIES_RATING, data, INSERT_BATCH_SIZE)


conn.commit()
conn.close()