import os
from dotenv import find_dotenv, load_dotenv

from clickhouse_driver import Client

load_dotenv(find_dotenv())


def init_clickhouse_db():
    shards = [['1', '2', '3'], ['2', '3', '1'], ['3', '1', '2']]
    for ctr, node in enumerate(['1', '4', '7']):
        client = Client(host=os.getenv(f'NODE_{node}_HOST'), port=os.getenv(f'NODE_{node}_PORT'))
        client.execute('CREATE DATABASE shard;')
        client.execute('CREATE DATABASE replica1;')
        client.execute('CREATE DATABASE replica2;')
        client.execute(f"CREATE TABLE shard.views (user_id String, movie_id String, value_timestamp DateTime) \
        Engine=ReplicatedMergeTree('/clickhouse/tables/shard{shards[ctr][0]}/views', 'replica_1') \
        PARTITION BY toYYYYMMDD(value_timestamp) ORDER BY value_timestamp;")
        client.execute(f"CREATE TABLE replica1.views (user_id String, movie_id String, value_timestamp DateTime) \
        Engine=ReplicatedMergeTree('/clickhouse/tables/shard{shards[ctr][1]}/views', 'replica_2') \
        PARTITION BY toYYYYMMDD(value_timestamp) ORDER BY value_timestamp;")
        client.execute(f"CREATE TABLE replica2.views (user_id String, movie_id String, value_timestamp DateTime) \
        Engine=ReplicatedMergeTree('/clickhouse/tables/shard{shards[ctr][2]}/views', 'replica_3') \
        PARTITION BY toYYYYMMDD(value_timestamp) ORDER BY value_timestamp;")
        client.execute("CREATE TABLE default.views (user_id String, movie_id String, value_timestamp DateTime) \
        ENGINE = Distributed('company_cluster', '', views, rand());")


if __name__ == '__main__':
    init_clickhouse_db()
