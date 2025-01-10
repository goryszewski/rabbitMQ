import pika


class Queue:
    def __init__(
        self, host, user, password, queue, auto_ack=True, durable=True, exchange="", logger={}, arguments={}, exchange_type=[]
    ) -> None:
        self.host = host
        self.queue = queue
        self.user = user
        self.password = password
        self.routing_key = queue

        self.durable = durable
        self.auto_ack = auto_ack
        self.exchange = exchange
        self.routing_keys = []
        self.exchange_type = exchange_type
        self.arguments = arguments
        self.logger = logger
        self.init = False
        self.__prep()

    def __prep(self) -> None:
        self.__connect()
        if self.init:
            self.__channel()
            self.__initRMQ()
        
        if self.exchange:
            self.__initEXCH()
            self.__bind()


    def __connect(self) -> None:
        try:
            credentials = pika.PlainCredentials(self.user, self.password)

            parameters = pika.ConnectionParameters(credentials=credentials, host=self.host)

            self.conn = pika.BlockingConnection(parameters)
            self.init = True
        except Exception as e:
            if self.logger:
                self.logger.error(e)
            self.init = False

    def __channel(self) -> None:
        self.channel = self.conn.channel()

    def __initRMQ(self) -> None:
        self.channel.queue_declare(queue=self.queue, arguments=self.arguments, durable=self.durable)

    def __initEXCH(self) -> None:
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)

    def __bind(self) -> None:
        for routing_key in self.routing_keys:
            self.channel.queue_bind(exchange=self.exchange, queue=self.queue, routing_key=routing_key)

    def send(self, body) -> bool:
        if self.init:
            try:
                self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=body)
            except Exception as e:
                if self.logger:
                    self.logger.error("ERROR send")
                    self.logger.error(e)
                self.__prep()
                return False
            return True
        self.__prep()
        if self.logger:
            self.logger.error("No init")
        return False

    def recv(self, callback):
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=self.auto_ack)
        self.channel.start_consuming()

    def __del__(self) -> None:
        self.conn.close()
