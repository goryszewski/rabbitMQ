import pika

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("host", help="host rabbitmq")
args=parser.parse_args()

HOST=args.host


def init_connection(host):
    return pika.BlockingConnection(pika.ConnectionParameters(host=host))


def callback(ch, method, properties, body):
    # print(ch)
    # print(method)
    # print(properties)
    print(f"callback body: {body}")

def recv(channel):
    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def main():
    con = init_connection(HOST)
    channel=con.channel()
    recv(channel=channel)

if __name__ == "__main__":
    main()