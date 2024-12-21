import pika

class Queue:
    def __init__(self,host,queue):
        self.host=host
        self.queue=queue

        self.__connect()

        self.__channel()

    def __connect(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))

    def __channel(self):
        self.channel= self.conn.channel()
        self.channel.queue_declare(queue=self.queue)

    def send(self,body):
        self.channel.basic_publish(exchange='',routing_key="hello",body=body)

    def recv(self,callback):
        print("test")
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def __del__(self):
        self.conn.close()
