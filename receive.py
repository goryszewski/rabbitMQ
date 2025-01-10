from lib.rabbit import Queue
import json, os
from dotenv import load_dotenv
from lib.schema import PayloadSchema
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)
payload_Schema = PayloadSchema()


def callbackACK(ch, method, properties, body):
    data = json.loads(body)
    print(f"method:{method}")
    print(f"callback body: {data}")
    error = payload_Schema.validate(data)
    if error:
        print(f"no ACK:{error}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    print("ack")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback(ch, method, properties, body):
    print(f"callback body: {body}")
    # DOTO write galera


def main():
    print(
        os.environ.get("RABBITMQ_QUEUE_NAME"),
    )
    objectQ = Queue(
        host=os.environ.get("RABBITMQ_HOST"),
        user=os.environ.get("RABBITMQ_USER"),
        password=os.environ.get("RABBITMQ_PASS"),
        queue=os.environ.get("RABBITMQ_QUEUE_NAME"),
        arguments={"x-queue-type": "quorum"},
        logger=logging,
        exchange=os.environ.get("RABBITMQ_EXCHANGE"),  # "logs",
        exchange_type=os.environ.get("RABBITMQ_EXCHANGE_TYPE"),  # "fanout",
    )
    print("test")
    objectQ.recv(callback=callback)


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(e)
