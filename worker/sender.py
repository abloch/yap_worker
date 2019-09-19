import os
import sys
import csv
import json
import pika
import time


def get_channel():
    rabbit_host = os.environ.get("RABBIT_HOST", "rabbit")
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))

    channel = connection.channel()
    channel.queue_declare(queue='to_yap')
    return channel, connection

def send_message(msg, channel):
    channel.basic_publish(
        exchange='',
        routing_key='to_yap',
        body=msg        
    )
    print(" [x] Sent '{}'".format(len(msg)))

def strip_tweet(tweet):
    return {
        "id": tweet["id"],
        "text": tweet['clean_text'],
        "original_text": tweet["tweet"],
        "created_at": tweet["created_at"],
        "username": tweet["username"],
        "time": tweet["time"],
        "urls": tweet["urls"],
        "date": tweet["date"],
    }

def process_tweet(tweet,channel):
    # stripped = strip_tweet(tweet)
    msg = json.dumps(tweet)
    send_message(msg, channel)


if __name__ == "__main__":
    channel, connection = get_channel()
    inputfilename = sys.argv[1]
    if not os.path.isfile(inputfilename):
        print("not such file {}".format(inputfilename))
        sys.exit(1)

    inputfile = open(inputfilename)
    input = list(csv.DictReader(inputfile)) if inputfilename.endswith(".csv") else json.load(inputfile)
    
    limit = os.environ.get("LIMIT")
    if limit:
        limit = int(limit)
        print("sending only first {}".format(limit))

    for tweet in input[:limit]:
        process_tweet(tweet, channel)
    connection.close()
    print("I'm done here")
    while True:
        time.sleep(10)
