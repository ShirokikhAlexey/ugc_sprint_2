from clickhouse_driver import Client

CLICKHOUSE_HOST = 'localhost'
KAFKA_HOST_AND_PORT = 'broker:29092'

client = Client(host=CLICKHOUSE_HOST)

print(client.execute('SHOW DATABASES'))

client.execute(
    'CREATE DATABASE IF NOT EXISTS test_kafka ON CLUSTER company_cluster'
)

client.execute(
    '''CREATE TABLE IF NOT EXISTS test_kafka.views ON CLUSTER company_cluster
(
    user_id String,
    movie_id String,
    value_timestamp DateTime,
    created_at DateTime
) ENGINE = MergeTree
PARTITION BY toYYYYMM(created_at)
ORDER BY created_at;
'''
)

client.execute(f'''
CREATE TABLE if not exists kafka_queue (
    value FixedString(10)
  ) ENGINE = Kafka SETTINGS
    kafka_broker_list = '{KAFKA_HOST_AND_PORT}',
    kafka_topic_list = 'views',
    kafka_group_name = 'clickhouse_views',
    kafka_format = 'RowBinary',
    kafka_row_delimiter = '\n'
''')

client.execute('''
CREATE MATERIALIZED VIEW IF NOT EXISTS views_consumer TO test_kafka.views
AS SELECT substring(_key, 1, 6) AS user_id,
substring(_key, 8, 16) AS movie_id,
toDateTime(value) as value_timestamp,
_timestamp as created_at
FROM kafka_queue;
''')
