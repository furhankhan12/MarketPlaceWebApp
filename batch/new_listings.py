# pulls new listing messages from Kafka and indexes them in ES
import json
from time import sleep
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

sleep_time = 2
# print(sleep_time)
retries = 4
# strerror = None

for x in range(0, retries):  
    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        print("consumer", consumer)
        es = Elasticsearch(['es'])

        while (True):
            for message in consumer:
                new_listing = json.loads((message.value).decode('utf-8'))
                print("batch new listing", new_listing)
                es.index(index='listing_index', doc_type='listing', id=new_listing['id'], body=new_listing)
                # indicies.refresh might have to happen first?
                es.update(index='listing_index', doc_type='listing', id=new_listing['id'], body={ 'script' : 'ctx._source.visits = 0'})

            es.indices.refresh(index="listing_index")
        
        strerror = None
        # print(strerror)

    # except Exception as strerror:
    except:
        strerror = "error"
        # strerror = Exception
        # print(strerror)
        # strerror = strerror
        pass

    finally:
        if strerror:
            print("sleeping for", sleep_time)
            print("error", strerror)
            sleep(sleep_time)  # wait before trying to fetch the data again
            sleep_time *= 2  # Implement your backoff algorithm here i.e. exponential backoff
        else:
            break
    