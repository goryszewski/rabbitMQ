import pika


class Queue:
    def __init__(
        self,
        host,
        user,
        password,
        logger,
        queue=None,
        routing_key="",
        auto_ack=True,
        durable=True,
        exchange="",
        arguments={},
        exchange_type: str = "",
    ) -> None:
        self.host = host
        self.queue = queue
        self.user = user
        self.password = password
        self.routing_key = routing_key

        self.durable = durable
        self.auto_ack = auto_ack
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.arguments = arguments
        self.logger = logger
        self.init = False
        self.__prep()

    def __prep(self) -> None:
        queue = None
        self.__connect()
        if self.init:
            self.__channel()
            if self.queue:
                queue = self.__initRMQ()
                self.logger.info("Create queue")

            if self.exchange:
                self.__initEXCH()
            if queue and self.exchange:
                self.__bind(queue.method.queue)

    def __connect(self) -> None:
        try:
            credentials = pika.PlainCredentials(self.user, self.password)

            parameters = pika.ConnectionParameters(credentials=credentials, host=self.host)

            self.conn = pika.BlockingConnection(parameters)
            self.init = True
        except Exception as e:
            self.logger.error(e)
            self.init = False

    def __channel(self) -> None:
        self.channel = self.conn.channel()

    def __initRMQ(self):
        result = self.channel.queue_declare(queue=self.queue, arguments=self.arguments, durable=self.durable)
        self.logger.info(f"Init:__initRMQ Queue={self.queue} arguments={self.arguments}")
        return result

    def __initEXCH(self) -> None:
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=self.durable)
        self.logger.info(f"Init:__initEXCH: {self.exchange} - {self.exchange_type}")

    def __bind(self, queue) -> None:
        self.channel.queue_bind(exchange=self.exchange, queue=queue)
        self.logger.info(f"Init:__bind exchange={self.exchange}, queue={queue}")

    def send(self, message, routing_key) -> bool:
        if self.init:
            try:
                r_key = routing_key if routing_key else self.routing_key
                self.logger.info(self.routing_key)
                self.channel.basic_publish(exchange=self.exchange, routing_key=r_key, body=message)
            except Exception as e:
                self.logger.error("ERROR send")
                self.logger.error(e)
                self.__prep()
                return False
            return True
        self.__prep()
        self.logger.error("No init")
        return False

    def recv(self, callback):
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=self.auto_ack)
        self.channel.start_consuming()

    def __del__(self) -> None:
        self.conn.close()
