from kafka import KafkaProducer

from event_producer.abstract_event_producer import EventProducer
from db import get_kafka


class KafkaEventProducer(EventProducer):

    def __init__(self, producer: KafkaProducer):
        self.producer = producer

    async def send(self, topic: str, key: bytes, value: bytes):
        result = self.producer.send(topic=topic, key=key, value=value)
        return result

    async def send_and_wait(self, topic: str, key: bytes, value: bytes):
        result = await self.producer.send_and_wait(topic=topic, key=key, value=value)
        return result


def get_kafka_event_producer() -> KafkaEventProducer:
    return KafkaEventProducer(producer=get_kafka.kafka_producer)
