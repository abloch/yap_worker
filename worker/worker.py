import os
import sys
import json
import pika
import requests
from preprocessor import preprocess

connection = None
channel = None
all_processed = []

def get_channel():
    rabbit_host = os.environ.get("RABBIT_HOST", "rabbit")
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
    connection.channel().queue_declare(queue='to_yap')
    connection.channel().queue_declare(queue='from_yap')
    return connection.channel()

def callback(ch, method, properties, body):
    print(" [x] Received {}".format(len(body)))
    process_message(body.decode(), channel=ch)
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

def get_yap(text):
    # return "..."
    payload = {
        "text": text + "  ",
    }
    yap_url = os.environ.get("YAP_URL", "http://localhost:80/yap/heb/joint")
    yap_host = os.environ.get("YAP_HOST", "yap")
    return requests.get(yap_url, json=payload, headers={"Host": yap_host}).json()

def submit_yapped(msg, channel):
    print("[*] - message {} submitted".format(msg.get('id', msg['text'])))
    channel.basic_publish(
	    exchange='',
        routing_key='from_yap',
        body=json.dumps(msg))

def submit_error(msg, channel):
    channel.basic_publish(
        exchange='',
        routing_key='yap_errors',
        body=json.dumps(msg))
    print("ERROR: [x] Sent '{}'".format(msg))

def get_morpgology(morph):
    slices = morph.split("|")
    return {
        slice.split('=')[0]: slice.split('=')[1] 
        for slice in slices if slice
    } 

def get_tokens(yap_reply):
    return [{
        "token": row.split('\t')[1],
        "root": row.split('\t')[2],
        "pos": row.split('\t')[3],
        "morphology": get_morpgology(row.split('\t')[5])
    } for row in yap_reply['dep_tree'].split('\n') if row]


def process_message(msg, channel=None): 
    slice = json.loads(msg)
    text = preprocess(slice['text'])
    reply = None
    yap_reply = get_yap(text)
    slice['tokens'] = get_tokens(yap_reply)
    slice['raw_yap'] = yap_reply
    submit_yapped(slice, channel)
    all_processed.append(slice)
        

def consume(channel):
    channel.basic_consume(
        queue='to_yap', 
        on_message_callback=callback
    ) 
    print(' [*] Waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    channel = get_channel()
    channel.queue_declare(queue='to_yap')
    consume(channel)
    connection.close()
