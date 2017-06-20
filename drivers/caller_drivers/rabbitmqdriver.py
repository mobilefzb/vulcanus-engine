import pika


class RabbitMQClient(object):

    def __init__(self, host):

        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.__channel = self.__connection.channel()

    def send_message(self, exchange_name, exchange_type, routing_key, message):

        self.__channel.exchange_declare(exchange=exchange_name,type=exchange_type)
        self.__channel.basic_publish(exchange=exchange_name,routing_key=routing_key,body=message)
        self.__connection.close()