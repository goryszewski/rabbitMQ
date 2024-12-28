from lib.rabbit import Queue
import argparse,json
from lib.schema import PayloadSchema

parser = argparse.ArgumentParser()
parser.add_argument("host", help="host rabbitmq")
args = parser.parse_args()
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
    data = json.loads(body)
    print(f"callback body: {data}")


def main():
    objectQ = Queue(host=args.host, queue="hello",auto_ack=False)
    objectQ.recv(callback=callbackACK)


if __name__ == "__main__":
    main()
