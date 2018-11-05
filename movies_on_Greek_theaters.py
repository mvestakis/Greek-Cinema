# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 00:21:15 2018

@author: marios.vestakis
"""

import requests
import psycopg2
import re

#Getting the now playing movies in Greek theaters
response = requests.get("https://api.themoviedb.org/3/movie/now_playing?api_key=a3996754a4947548e00ff6b6c1d5eedd&region=GR&language=el").json()
#results contains all the valuable information
mylist = response['results']

for i in range(len(mylist)):
    title = re.sub('\'|\'', '\'\'', mylist[i]['title']) 
    desc = re.sub('\'|\'', '\'\'', mylist[i]['overview'])
    originalTitle = re.sub('\'|\'', '\'\'', mylist[i]['original_title'])
    id = str(mylist[i]['id'])
    response1 = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=a3996754a4947548e00ff6b6c1d5eedd&append_to_response=credits".format(id)).json()
    j = 0
    for j in range(len(response1['credits']['crew'])):
        if response1['credits']['crew'][j]['job'] == 'Director': #searching for director
            dName=response1['credits']['crew'][j]['name']
            response2 = requests.get("https://api.themoviedb.org/3/person/{}?api_key=a3996754a4947548e00ff6b6c1d5eedd".format(response1['credits']['crew'][j]['id'])).json()
            imdb_id = response2["imdb_id"]
            if imdb_id == '':
                    imdb = 'Imdb profile is not provided'                
            else:
                    imdb = 'https://www.imdb.com/name/'+imdb_id+'/?ref_=tt_ov_dr'
            from psycopg2 import Error
            try:
                #providing the authentication needed in order to connect to the DB 
                connection = psycopg2.connect(database="movie_info", 
                                 user = "postgres", 
                                 password = "xaroupies7", 
                                 host = "localhost", 
                                 port = "5432")
                
                cursor = connection.cursor()
                if i == 0:
                    postgres_insert_query_zero = """ DELETE FROM directors"""
                    cursor.execute(postgres_insert_query_zero)
                    postgres_insert_query_one = """ DELETE FROM movies"""
                    cursor.execute(postgres_insert_query_one)
                #all the data for every movie are stored in a table in a postgreSQL DB 
                
                postgres_insert_query_two = """ INSERT INTO movies VALUES ('{}','{}','{}');""".format(title,desc,originalTitle)
                
                postgres_insert_query_three = """ INSERT INTO directors VALUES ('{}','{}','{}');""".format(originalTitle,dName,imdb)
                
                cursor.execute(postgres_insert_query_three)
                connection.commit()

                cursor.execute(postgres_insert_query_two)
                connection.commit()
                
                print ("Records inserted successfully into mobile")
            #in case of error!    
            except (Exception, psycopg2.DatabaseError) as error :
                if(connection):
                    connection.rollback()
                print("Failed inserting record into mobile table {}".format(error))
            finally:
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")        
            print("\n")
