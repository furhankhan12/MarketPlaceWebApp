# that periodically parses the log and updates the view counts in ES
# this one def isn't ready

from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['es'])

f = open("view_log.txt", "r")
for line in f:
    # {user_id, item_id}
    es.update(index='listing_index', doc_type='listing', id=line[1] , body={ 'script' : 'ctx._source.visits += 1'})

    # and then delete the thing from the log so that it doesn't count it every time?

f.close()