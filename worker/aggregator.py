import os
import sys
import json
import csv
from io import StringIO
import pika
import requests

connection = None
channel = None
outfile = open(os.environ["OUTFILE"], "a")

def get_channel():
    rabbit_host = os.environ.get("RABBIT_HOST", "rabbit")
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
    connection.channel().queue_declare(queue='from_yap')
    return connection.channel()

def callback(ch, method, properties, body):
    print(" [x] Received {}".format(len(body)))
    process_message(body.decode(), channel=ch)
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

def process_message(msg, channel=None): 
    outfile.write(msg + ",\n")

def consume(channel):
    channel.basic_consume(
        queue='from_yap', 
        on_message_callback=callback
    ) 
    print(' [*] Waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    channel = get_channel()
    channel.queue_declare(queue='from_yap')
    consume(channel)
    connection.close()
