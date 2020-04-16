# pulls new listing messages from Kafka and indexes them in ES
import json
import time
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

print("outside of retries")
sleep_time = 2
retries = 4
for x in range(0, retries):  
    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        print("consumer", consumer)
        es = Elasticsearch(['es'])
        print(es.info())

        while (True):
            for message in consumer:
                new_listing = json.loads((message.value).decode('utf-8'))
                print("new listing", new_listing)
                es.index(index='listing_index', doc_type='listing', id=new_listing['id'], body=new_listing)
                # indicies.refresh might have to happen first?
                es.update(index='listing_index', doc_type='listing', id=new_listing['id'], body={ 'script' : 'ctx._source.visits = 0'})

            es.indices.refresh(index="listing_index")
            print("refresh reached")
        
        strerror = None

    except:
        strerror = "error"
        pass

    finally:
        if strerror:
            print("sleeping for", sleep_time)
            print(strerror)
            time.sleep(sleep_time)  # wait before trying to fetch the data again
            sleep_time *= 2  # Implement your backoff algorithm here i.e. exponential backoff
        else:
            break
    