import pika

class consumer(object):
    def __init__(self, **kwargs):        
        self.exchange = kwargs['exchange']        

    def recieve(self):
        credentials = pika.PlainCredentials('guest', 'guest')

        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='rabbitmq_host',credentials=credentials))

        channel = connection.channel()        
        result = channel.exchange_declare(exchange=self.exchange,type='topic',durable=True)
        
        queue_name = 'your queue name'

        channel.queue_bind(exchange=self.exchange,
                           queue=queue_name,
                           routing_key='topic/topic_name')

        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(" [x] %r:%r" % (method.routing_key, body))


        channel.basic_consume(callback,
                              queue=queue_name,
                              no_ack=True)

        channel.start_consuming()
