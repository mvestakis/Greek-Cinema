First open an administration and development platform for PostgreSQL
and run the queries:

1)CREATE DATABASE movie_info;

2)CREATE TABLE IF NOT EXISTS movies ( title   TEXT PRIMARY KEY,
                                      descr 			  TEXT,
                              originalTitle 			  TEXT)
							  
							  

  CREATE TABLE IF NOT EXISTS directors (  originalTitle   TEXT,
									      dName           TEXT,
                                          imdb  		  TEXT)

									 
Now that the database and the tables are created simply run the 
movies_on_Greek_theaters.py script and find out which movies are on Greek
theaters!