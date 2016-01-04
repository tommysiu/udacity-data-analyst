#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import json

# Get the MongoDB database instance by name
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

# Insert the JSON file into a collection of the 'osm' database
def insert_data(json_file, col_name):
    db = get_db('osm')
    with open(json_file) as f:
        data = json.loads(f.read())
        db[col_name].insert(data)

# Utility function to lookup nodes by housenumber pattern and add address.place accordingly 
def update_nodes_place(collection,place,regex='.*'):
    result = find_nodes_by_housenumber(collection,regex)
    for n in result:
        id = n['id']
        housenumber = n['address']['housenumber']
        n['address']['place'] = place
        collection.save(n)
        print "Place has been added for node[%s] with housenumber[%s]." % (id, housenumber)

# Utility function to lookup nodes by housenumber pattern and add address.street accordingly 
def update_nodes_street(collection,street,regex='.*'):
    result = find_nodes_by_housenumber(collection,regex)
    for n in result:
        id = n['id']
        housenumber = n['address']['housenumber']
        n['address']['street'] = street
        collection.save(n)
        print "Street has been added for node[%s] with housenumber[%s]." % (id, housenumber)

# Utility function to lookup nodes by document ids and add address.place accordingly 
def update_nodes_place_by_id(collection,place,ids):
    result = find_nodes_by_id(collection,ids)
    for n in result:
        id = n['id']
        housenumber = n['address']['housenumber']
        n['address']['place'] = place
        collection.save(n)
        print "Place has been added for node[%s] with housenumber[%s]." % (id, housenumber)

# Utility function to lookup nodes by document ids and add address.street accordingly 
def update_nodes_street_by_id(collection,street,ids):
    result = find_nodes_by_id(collection,ids)
    for n in result:
        id = n['id']
        housenumber = n['address']['housenumber']
        n['address']['street'] = street
        collection.save(n)
        print "Street has been added for node[%s] with housenumber[%s]." % (id, housenumber)

# This function finds all nodes with addr:housenumber but not addr:street or addr:place.
# The housenumber must match the regular expression argument. By default it matches any string.
def find_nodes_by_housenumber(collection,regex='.*'):
    result = collection.find({
        'doc_type':'node',
        '$and':[
        {'address.housenumber':{'$exists':1}},
        {'address.housenumber':{'$regex':regex}}
        ],
        'address.street':{'$exists':0},
        'address.place':{'$exists':0}
        })
    return result

# This function finds all nodes with id in the passed array.
def find_nodes_by_id(collection,ids):
    result = collection.find({
        'doc_type':'node',
        'id':{'$in':ids}
        })
    return result

