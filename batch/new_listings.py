# pulls new listing messages from Kafka and indexes them in ES
import json, time
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

sleep_time = 2
retries = 5
for x in range(0, retries):  
    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        es = Elasticsearch(['es'])

        while (True):
            for message in consumer:
                new_listing = json.loads((message.value).decode('utf-8'))
                es.index(index='listing_index', doc_type='listing', id=new_listing['id'], body=new_listing)
                es.update(index='listing_index', doc_type='listing', id=new_listing['id'], body={ 'script' : 'ctx._source.visits = 0'})
                print(new_listing)

            es.indices.refresh(index="listing_index")
        
        strerror = None
    except:
        strerror = "error"
        pass

    if strerror:
        print("new: sleeping for", sleep_time)
        time.sleep(sleep_time)
        sleep_time *= 2  
    else:
        break
    