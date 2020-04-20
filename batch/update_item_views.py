# that periodically parses the log and updates the view counts in ES
# this one def isn't ready

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
        print("sleeping for", sleep_time)
        time.sleep(sleep_time)
        sleep_time *= 2 
    else:
        break

if es:
    f = open("view_log.txt").read().splitlines()
    for line in f:
        # format is
        # user_id item_id
        # split = line.split()
        item_id = int(line.split()[1])
        print(line.split()[1])
        es.update(index='listing_index', doc_type='listing', id=item_id , body={ 'script' : 'ctx._source.visits += 1'})
            
        # and then delete the thing from the log so that it doesn't count it every time???