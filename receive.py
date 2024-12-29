from lib.rabbit import Queue
import json, os
from dotenv import load_dotenv
from lib.schema import PayloadSchema

load_dotenv()

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


def main():
    objectQ = Queue(
        host=os.environ.get("RABBITMQ_HOST"),
        queue=os.environ.get("RABBITMQ_QUEUE_NAME"),
        user=os.environ.get("RABBITMQ_USER"),
        password=os.environ.get("RABBITMQ_PASS"),
    )
    objectQ.recv(callback=callback)


if __name__ == "__main__":
    main()
