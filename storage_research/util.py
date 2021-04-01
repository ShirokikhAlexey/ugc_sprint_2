from functools import wraps
from time import time, sleep

from itertools import product
from random import randint

def time_it(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time()
        f(*args, **kwds)
        end = time()
        diff = round(end - start, 3)
        return diff
    return wrapper

def generate_movie_user(movie_size: int, user_size: int):
    return product(range(movie_size), range(user_size))

def generate_movie_rating(user_size: int, movie_count: int):
    data = iter([tuple(list(item) + [randint(0, 10)]) for item in product(range(user_size), range(movie_count))])
    return data

def generate_movie_rating_mongo(user_size: int, movie_count: int):
    data = iter([{"user_id": item[0],
                  "movie_id": item[1],
                  "rating": randint(0, 10)}
                  for item in product(range(user_size), range(movie_count))])
    return data

# l = generate_movie_rating_mongo(10, 10)
# print(list(l))