### This module will use the csv files created using the data.py to create a database in sqlite. 

import sqlite3
import csv
from pprint import pprint

##Connect to the database or create new database if doesn't already exist
sqlite_file = 'OSM_FINAL_DB.db'
conn = sqlite3.connect(sqlite_file)
conn.text_factory = str #if using 8-bit strings instead of unicode string in sqlite3, set approptiate text_factory for sqlite connection

##Create a cursor object
cur = conn.cursor()

##Drop nodes tables if already exists   
cur.execute("DROP TABLE IF EXISTS nodes;")
conn.commit()

##Create the table specifying the column names and data types
cur.execute("CREATE TABLE nodes(id, lat, lon, user, uid, version, changeset, timestamp);")
conn.commit()

##Reading data
with open('nodes.csv', 'rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['lat'], i['lon'], i['user'],i['uid'],i['version'],i['changeset'],i['timestamp']) for i in dr]

    
    cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    conn.commit()

#Drop nodes_tags table if already exists   
cur.execute("DROP TABLE IF EXISTS nodes_tags")
conn.commit()


##create nodes_tags table
cur.execute("CREATE TABLE nodes_tags (id, key, value, type);")
with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
conn.commit()


#Drop ways table if already exists   
cur.execute("DROP TABLE IF EXISTS ways")
conn.commit()

##Create ways table
cur.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
with open('ways.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
conn.commit()

#Drop ways_nodes table if already exists   
cur.execute("DROP TABLE IF EXISTS ways_nodes")
conn.commit()

##Create ways_nodes table
cur.execute("CREATE TABLE ways_nodes (id, node_id, position);")
with open('ways_nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)
conn.commit()


#Drop ways_tags table if already exists   
cur.execute("DROP TABLE IF EXISTS ways_tags")
conn.commit()

##Create ways_tags table
cur.execute("CREATE TABLE ways_tags (id, key, value, type);")
with open('ways_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
conn.commit()

conn.close()
