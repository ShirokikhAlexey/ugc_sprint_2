import os
import random
from datetime import datetime
import time
from dotenv import find_dotenv, load_dotenv

from clickhouse_driver import Client

load_dotenv(find_dotenv())

CLICKHOUSE_HOST = 'localhost'

client = Client(host=CLICKHOUSE_HOST)

num_rows = int(os.getenv('num_rows'))
batch_size = int(os.getenv('batch_size'))


def gen_rows(number):
    for _ in range(number):
        user_id = f"'{random.randrange(100000, 200000, 1)}'"
        movie_id = f"'tt{random.randrange(1000000, 1100000, 1)}'"
        val = f'{random.randrange(1, 14400, 1)}'
        yield user_id, movie_id, val


if __name__ == '__main__':
    rows = gen_rows(num_rows)
    ctr = 0
    batch = []
    time_list = []
    print(f'Start')
    print(time.time())
    start_all = time.time()
    for user_id, movie_id, val in rows:
        ctr += 1
        batch.append(f'({user_id}, {movie_id}, {val}, {datetime.now().timestamp()})')
        if ctr % batch_size == 0:
            print(ctr)
            start = time.time()
            client.execute(f'''
                        INSERT INTO test_kafka.views
                        (user_id, movie_id, value_timestamp, created_at)
                        VALUES {','.join(batch)};
                        ''')
            end = time.time() - start
            print(end)
            time_list.append(end)
            batch = []
    print(f'Total time: {time.time() - start_all}')
    print(f'Batch size: {batch_size}')
    print(f'Num rows: {num_rows}')
    print(f'Mean insert time: {sum(time_list)/int(num_rows/batch_size)}')
