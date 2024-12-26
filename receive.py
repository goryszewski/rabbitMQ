from lib.rabbit import Queue
import argparse,json

parser = argparse.ArgumentParser()
parser.add_argument("host", help="host rabbitmq")
args = parser.parse_args()


def callbackACK(ch, method, properties, body):
    print(f"callback body: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"callback body: {data}")


def main():
    objectQ = Queue(host=args.host, queue="hello")
    objectQ.recv(callback=callback)


if __name__ == "__main__":
    main()
