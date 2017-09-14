import sqlite3
#Connect to database
db = sqlite3.connect("OSM_FINAL_DB.db")
cur = db.cursor()

## Number of nodes
cur.execute("SELECT COUNT(*) FROM nodes;")
nodes = cur.fetchall()
nodes


## Number of ways
cur.execute("SELECT COUNT(*) FROM ways;")
ways = cur.fetchall()
ways

cur.execute("DROP TABLE IF EXISTS users;")
db.commit()

##Number of Unique Users

"""cur.execute( "SELECT COUNT(DISTINCT(all_uid.uid)) FROM 
                (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) as all_uid; ")
num_users = cur.fetchall()
num_users """

## OR 

cur.execute(""" CREATE TABLE users AS
                SELECT all_uid.user AS user_name, all_uid.uid AS user_id
                FROM 
                (SELECT user, uid FROM nodes 
                UNION ALL
                SELECT user, uid FROM ways) all_uid; """)
db.commit()

cur.execute(""" SELECT COUNT(DISTINCT(user_id)) FROM users; """)
cur.fetchall()

## Top 10 Users

top_10 = cur.execute(""" SELECT user_name, user_id, COUNT(user_id) AS contributions 
                FROM users
                GROUP BY user_id
                ORDER BY contributions DESC
                LIMIT 10; """).fetchall()
top_10

#Top 10 Users using pandas
import pandas as pd

top_10_df = pd.read_sql_query(""" SELECT user_name, user_id, COUNT(user_id) AS contributions 
                FROM users
                GROUP BY user_id
                ORDER BY contributions DESC
                LIMIT 10; """, db)
top_10_df


#One-time users

cur.execute(""" 
            SELECT COUNT(*) 
            FROM
                (SELECT user_id, COUNT(user_id) as num 
                FROM users
                GROUP BY user_id
                HAVING num = 1) one_time_users; """)
one_time_users = cur.fetchall()
one_time_users

#### Looking at Postcodes

cur.execute("""SELECT tags.value, COUNT(*) as count 
    FROM (SELECT * FROM nodes_tags 
    UNION ALL 
    SELECT * FROM ways_tags) tags
    WHERE tags.key='postcode'
    GROUP BY tags.value
    ORDER BY count DESC;""")
cur.fetchall()



# There are three problematic postcodes 
# 1) postcode = 'Weslayan Street" 
# 2) postcode = 88581 - This doesn't look like Houston Area postcode as Houston Area postcodes start with 7
# 3) postcode = '7'

# Looking at postcode 88581

prob_postcode_details = cur.execute("""SELECT *
            FROM nodes 
            WHERE id IN (SELECT DISTINCT(id) FROM nodes_tags WHERE key='postcode' AND value='88581');""").fetchall()

prob_postcode_details
# getting address details by using the id from above results

prob_postcode = cur.execute("""SELECT * FROM nodes_tags WHERE id='1924194015';""").fetchall()
prob_postcode

# this address is in la porte, texas. Using the address Supercuts, 9001 Spencer Hwy d, La Porte, the postcode comes out to be 77571 instead of 88581.
# getting address details by using the id from above results

cur.execute(""" UPDATE nodes_tags
                SET value = '77571' 
                WHERE id = '1924194015' AND  key = 'postcode' AND value = '88581'; """)
db.commit()

# Looking at postcode Weslayan Street

prob_postcode2_details = cur.execute("""SELECT *
            FROM nodes_tags
            WHERE id IN (SELECT DISTINCT(id) FROM nodes_tags WHERE key='postcode' AND value='Weslayan Street');""").fetchall()

prob_postcode2_details
# It seems like postcode is in place of street and street in place of postcode. 
#We will need to modify our update_postcode function to correct both of these postcodes. or modify table in sqlite

cur.execute("""UPDATE nodes_tags 
    SET value = CASE 
    WHEN key = 'street' 
        THEN 'Weslayan Street' 
    WHEN key = 'postcode' 
        THEN '77027' 
    ELSE value 
    END
WHERE  id = '1812187787';""")
db.commit()

#Looking at postcode '7-'
prob_postcode3_details = cur.execute("""SELECT *
            FROM nodes_tags
            WHERE id IN (SELECT DISTINCT(id) FROM nodes_tags WHERE key='postcode' AND value='7-');""").fetchall()

prob_postcode3_details

# PCorrect postcode is 77478 for the address we got from above query
cur.execute(""" UPDATE nodes_tags
                SET value = '77478' 
                WHERE id = '4265057550' AND  key = 'postcode' AND value = '7-'; """)
db.commit()

# A look at all the cities
cur.execute("""SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key LIKE '%city' 
GROUP BY tags.value
ORDER BY count DESC;""").fetchall()

# Lookint at amenities

amen_df = pd.read_sql_query("""SELECT value, COUNT(*) as num
                            FROM nodes_tags
                            WHERE key='amenity'
                            GROUP BY value
                            ORDER BY num DESC
                            LIMIT 10;""", db)
amen_df

#Religion
religion = cur.execute("""SELECT nodes_tags.value, COUNT(*) as num
                        FROM nodes_tags 
                        JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
                        ON nodes_tags.id=i.id
                        WHERE nodes_tags.key='religion'
                        GROUP BY nodes_tags.value
                        ORDER BY num DESC;""").fetchall()
religion

#Cuisine
cuisine = cur.execute("""SELECT nodes_tags.value, COUNT(*) as num
                        FROM nodes_tags 
                        JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
                        ON nodes_tags.id=i.id
                        WHERE nodes_tags.key='cuisine'
                        GROUP BY nodes_tags.value
                        ORDER BY num DESC
                        LIMIT 10;""").fetchall()
cuisine

#source of data
cur.execute("DROP TABLE IF EXISTS allsources;")

cur.execute(""" CREATE TABLE allsources AS
                SELECT value, count(*) AS num
                FROM
                (SELECT value 
                FROM nodes_tags
                WHERE nodes_tags.key = 'source'
                GROUP BY value
                        
                UNION ALL
                        
                SELECT value 
                FROM ways_tags
                WHERE ways_tags.key = 'source'
                GROUP BY value) source
                GROUP BY source.value;""")
# Source Bing
cur.execute(""" SELECT SUM(num) AS Bing
                FROM
                (SELECT * FROM allsources
                WHERE value LIKE 'Bing%' OR value LIKE '%bing%') b""").fetchall()

#Source Google
cur.execute(""" SELECT SUM(num) AS google
                FROM
                (SELECT * FROM allsources
                WHERE value LIKE 'Google%' OR value LIKE '%google%') g""").fetchall()
# Source - Tiger
cur.execute(""" SELECT SUM(num) AS tiger
                FROM
                (SELECT * FROM allsources
                WHERE value LIKE 'Tiger%' OR value LIKE '%tiger%') t""").fetchall()


