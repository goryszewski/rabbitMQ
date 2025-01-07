import pika


class Queue:
    def __init__(
        self,
        host,
        user,
        password,
        queue,
        auto_ack=True,
        durable=True,
        exchange="",
        arguments={},
    ) -> None:
        self.host = host
        self.queue = queue
        self.user = user
        self.password = password
        self.routing_key = queue

        self.durable = durable
        self.auto_ack = auto_ack
        self.exchange = exchange
        self.arguments = arguments

        self.__connect()
        self.__channel()
        self.__initRMQ()

    def __connect(self) -> None:
        credentials = pika.PlainCredentials(self.user, self.password)

        parameters = pika.ConnectionParameters(credentials=credentials, host=self.host)

        self.conn = pika.BlockingConnection(parameters)

    def __channel(self) -> None:
        self.channel = self.conn.channel()

    def __initRMQ(self) -> None:
        self.channel.queue_declare(queue=self.queue, arguments=self.arguments, durable=self.durable)

    def send(self, body):
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=body)

    def recv(self, callback):
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=self.auto_ack)
        self.channel.start_consuming()

    def __del__(self) -> None:
        self.conn.close()
