import os
from dotenv import find_dotenv, load_dotenv

from clickhouse_driver import Client

load_dotenv(find_dotenv())


def init_clickhouse_db():
    shards = [['1', '2', '3'], ['2', '3', '1'], ['3', '1', '2']]
    for ctr, node in enumerate([1, 4, 7]):
        client = Client(host=os.getenv(f'NODE_{node}_HOST'), port=os.getenv(f'NODE_{node}_PORT'))
        client.execute('CREATE DATABASE test_kafka;')
        client.execute('CREATE DATABASE shard;')
        client.execute(f"""CREATE TABLE shard.views 
            (user_id String, movie_id String, value_timestamp DateTime, created_at DateTime) \
            Engine=ReplicatedMergeTree('/clickhouse/tables/shard{shards[ctr][0]}/views', 'replica_1') \
            PARTITION BY toYYYYMM(created_at) ORDER BY created_at;""")
        client.execute("""CREATE TABLE test_kafka.views 
            (user_id String, movie_id String, value_timestamp DateTime, created_at DateTime) \
            ENGINE = Distributed('company_cluster', 'shard', views, rand());""")
        client.disconnect()

        client = Client(host=os.getenv(f'NODE_{node+1}_HOST'), port=os.getenv(f'NODE_{node+1}_PORT'))
        client.execute('CREATE DATABASE replica1;')
        client.execute(f"""CREATE TABLE replica1.views 
                    (user_id String, movie_id String, value_timestamp DateTime, created_at DateTime) \
                    Engine=ReplicatedMergeTree('/clickhouse/tables/shard{shards[ctr][1]}/views', 'replica_2') \
                    PARTITION BY toYYYYMM(created_at) ORDER BY created_at;""")
        client.disconnect()

        client = Client(host=os.getenv(f'NODE_{node + 2}_HOST'), port=os.getenv(f'NODE_{node + 2}_PORT'))
        client.execute('CREATE DATABASE replica2;')
        client.execute(f"""CREATE TABLE replica2.views 
                    (user_id String, movie_id String, value_timestamp DateTime, created_at DateTime) \
                    Engine=ReplicatedMergeTree('/clickhouse/tables/shard{shards[ctr][2]}/views', 'replica_3') \
                    PARTITION BY toYYYYMM(created_at) ORDER BY created_at;""")
        client.disconnect()


if __name__ == '__main__':
    init_clickhouse_db()