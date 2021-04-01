from time import sleep

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

producer.send(
    topic='views',
    value=b'1611039931',
    key=b'500271+tt0120338',
)

sleep(1)
