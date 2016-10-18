import pika
from pprint import pprint

class publisher (object):  
           
    def __init__(self,host=None,username=None,password=None):
        self.credentials = pika.PlainCredentials(username, password)                
        self.connection = None
        self.channel = None
        self.queue_name = None
        self.exchange = "event.topic"
        self.routing_key = "routing_key"
        self.host = host
   
    def connect(self):
        print ("trying to establish connection to {}".format(self.host))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,port=56772,credentials=self.credentials))
        
        self.channel = self.connection.channel()

    def publish(self,message):       
        
        self.channel.exchange_declare(exchange=self.exchange,
                         type='topic',durable=True)

        self.channel.queue_bind(exchange=self.exchange,
                                queue=self.queue_name)
        
        self.channel.basic_publish(exchange=self.exchange,
                              routing_key=self.queue_name,
                              body=message)
        print ("queue name is: {}".format(self.queue_name))
        print(" [x] Sent %r:%r" % (self.routing_key,message))

    def close_connection(self):    
        self.connection.close()
