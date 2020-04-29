# pulls item viewing messages from Kafka and appends them to a logs

# TO DO : make sure it actually writes to the log file?
import json, time
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
sleep_time = 3
retries = 5

time.sleep(60)
for x in range(0, retries):
    try:
        consumer = KafkaConsumer('track-views-topic', group_id='listing-logger', bootstrap_servers=['kafka:9092'])
        es = Elasticsearch(['es'])
        print("TRACK VIEWS IS READY")
        while (True):
            for message in consumer:
                # f = open("view_log.txt", "a")
                new_click = json.loads((message.value).decode('utf-8'))
                print("INSIDE THE TRACKER")
                print(new_click)
                item = int(str(new_click['item_id']))
                # to_write = str(new_click['user_id']) + " " + str(new_click['item_id'])
                # print(to_write)
                # f.write(str(to_write)+'\n')
                # f.close()
                es.update(index='listing_index', doc_type='listing', id=item, body={ 'script' : 'ctx._source.visits += 1'})
        strerror = None

    except Exception as e:
        print(e)
        print("track: sleeping for", sleep_time)
        print("in track item view")
        time.sleep(sleep_time)
        sleep_time *= 2 
        pass
    