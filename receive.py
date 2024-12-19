import pika

#static
HOST='local'

def init_connection(host):
    return pika.BlockingConnection(pika.ConnectionParameters(host=host))


def callback(ch, method, properties, body):
    print(f"callback body: {body}")

def recv(channel):
    channel.queue_declare(queue="test")
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def main():
    pass

if __name__ == "__main__":
    main()