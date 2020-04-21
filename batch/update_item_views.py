# that periodically parses the log and updates the view counts in ES

## TO DO : make this update "periodically"
from elasticsearch import Elasticsearch
import json, time

sleep_time = 2
retries = 5
for x in range(0, retries):  
    try:
        es = Elasticsearch(['es'])
        strerror = None
    except:
        strerror = "error"
        pass

    if strerror:
        print("update: sleeping for", sleep_time)
        time.sleep(sleep_time)
        sleep_time *= 2 
    else:
        break

if es:
    f = open("view_log.txt").read().splitlines()
    counts = {}
    for line in f:
        # format is
        # user_id item_id
        item_id = int(line.split()[1])
        if item_id in counts:
            counts[item_id] += 1
        else:
            counts[item_id] = 1
        print(line.split()[1])
    for item in counts:
        es.update(index='listing_index', doc_type='listing', id=item, body={ 'script' : {'inline':'ctx._source.visits = params.count', 'params':{'count':counts[item] }}})