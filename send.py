import pika
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("host", help="host rabbitmq")
args=parser.parse_args()

HOST=args.host

def init_connection(host):
    return pika.BlockingConnection(pika.ConnectionParameters(host=host))

def send():
    pass



def main():
    con = init_connection(HOST)
    channel = con.channel()
    channel.queue_declare(queue="hello")

    channel.basic_publish(exchange='',routing_key="hello",body="Hello World!")

    print(f"Send msg")
    con.close()



if __name__ == "__main__":
    main()