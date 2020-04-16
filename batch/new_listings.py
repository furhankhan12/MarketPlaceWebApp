# pulls new listing messages from Kafka and indexes them in ES
import json
import time
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch


def es_connect():
    connected = False
    es = Elasticsearch(['es'])
    while not connected:
        try:
            es.info()
            connected = True
        except ConnectionError:
            print("Elasticsearch not available yet, trying again in 2s...")
            time.sleep(2)
    return es

print("hey in batch outside of retries")
sleep_time = 2
retries = 4
# strerror = None
for x in range(0, retries):  
    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        print("consumer", consumer)
        print("hey in batch in try")
        es = es_connect()
        print(es.info())

        while (True):
            print("consumer", consumer)
            for message in consumer:
                print("hey in batch in loop")
                new_listing = json.loads((message.value).decode('utf-8'))
                print("batch new listing", new_listing)
                es.index(index='listing_index', doc_type='listing', id=new_listing['id'], body=new_listing)
                # indicies.refresh might have to happen first?
                es.update(index='listing_index', doc_type='listing', id=new_listing['id'], body={ 'script' : 'ctx._source.visits = 0'})

            es.indices.refresh(index="listing_index")
            print("refresh reached")
        
        strerror = None
        # print(strerror)

    # except Exception as strerror:
    except:
        strerror = "error"
        print("hey in batch in except")
        # strerror = Exception
        # print(strerror)
        # strerror = strerror
        pass

    finally:
        if strerror:
            print("sleeping for", sleep_time)
            print(strerror)
            # print("hey in batch in try")
            sleep(sleep_time)  # wait before trying to fetch the data again
            sleep_time *= 2  # Implement your backoff algorithm here i.e. exponential backoff
        else:
            break
    