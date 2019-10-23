import pika
import random


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='loan_queue')

def bank(n):
    
    application = {"Danske bank":10000, "Nordea":20000, "Jyske bank":30000, "cphbusiness bank":50000,"Andelsbanken":60000}
    loantypes = ["personal","enterpreneur","small business"]
    
    fitloans = random.choice(list(application))
   
    fitloantype = random.choice(loantypes)

    amount =  application[fitloans]    
    
    n = int(''.join(filter(str.isdigit, n)))
            
    if n <= amount:
        print("Loan is granted to requested criteria")
        #return fitloans, application[fitloans], fitloantype
    else:
        print("Loan not granted due to loan limit capacity")

    return fitloans, application[fitloans], fitloantype



def on_request(ch, method, props, body):
    n = str(body)
    fitbankname, fitamount, fitloantype = bank(n)
    #print("Application accepted:" , fitamount , "at " , fitbankname , "with loantype "  , fitloantype, " is granted")

    
    print(" [.] application is bank(%s)" % n)
    #response = bank(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(bank(n)))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='loan_queue', on_message_callback=on_request)

print(" [x] Awaiting potential loan requests")
channel.start_consuming()