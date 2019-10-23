import pika
import uuid
import random

class Banksloan(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='loan_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)



def loan(n):
    loanamount = 50000
    age = 35
    repaymenttime = 10
    monthly = True
    loanstype = "personal"
    
    return loanamount  

banksloan = Banksloan()

print(" [x] Application received for loan amount %r" % banksloan.call(50000))
response = banksloan.call(50000)

print(" [.] Application of loan is: %r by" % (response))
