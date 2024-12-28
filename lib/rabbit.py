import pika


class Queue:
    def __init__(self, host, queue, auto_ack=True, exchange="") -> None:
        self.host = host
        self.queue = queue
        self.routing_key = queue

        self.auto_ack = auto_ack
        self.exchange = exchange

        self.__connect()
        self.__channel()
        self.__initRMQ()

    def __connect(self) -> None:
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))

    def __channel(self) -> None:
        self.channel = self.conn.channel()

    def __initRMQ(self) -> None:
        self.channel.queue_declare(queue=self.queue)

    def send(self, body):
        self.channel.basic_publish(
            exchange=self.exchange, routing_key=self.routing_key, body=body
        )


    def recv(self, callback):

        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=callback, auto_ack=self.auto_ack
        )
        self.channel.start_consuming()

    def __del__(self) -> None:
        self.conn.close()
