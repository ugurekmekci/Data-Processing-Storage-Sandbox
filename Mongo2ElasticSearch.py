import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch

#this code performs batch operation

mongodb_client = MongoClient('') #mongodb://ip:port
es_client = Elasticsearch(['']) #http://ip:port

mdb = mongodb_client['mydb']

drop= es_client.indices.delete(index='indexone', ignore=[400, 404])
creat= es_client.indices.create(index='indexone', ignore=400)

data = mdb.mycollection.find()

#The loop below works for existing collection
#user needs to change vars under loop below
#or has to create a collection with same fields

for x in data:
    _time = x['time']
    _loc = x['loc']
    _usr = x['usr']
    _act = x['act']
    _prdct = x['prdct']

    doc = {
        'time': _time,
        'loc': _loc,
        'usr': _usr,
        'act': _act,
        'prdct': _prdct
    }

    #indexing logic may differ in according to type of operation.
    #check elasticsearch api in order to meet expectations
    res = es_client.index(index="indexone", doc_type="docs", body=doc) 
    time.sleep(0.2)

print("Done")