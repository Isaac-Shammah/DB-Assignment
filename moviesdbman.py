import csv

from cs50 import SQL

open("moviesdb.db","w").close()

db = SQL("sqlite:///moviesdb.db")

db.execute("CREATE TABLE movies (m_id INTEGER, title TEXT, PRIMARY KEY(m_id))")

db.execute("CREATE TABLE movie_genres (mg_id INTEGER, genre_id INTEGER, PRIMARY KEY(genre_id), FOREIGN KEY(mg_id) REFERENCES movies(m_id))")

db.execute("CREATE TABLE genres (movies_id INTEGER, genre TEXT, PRIMARY KEY(movies_id), FOREIGN KEY(movies_id) REFERENCES movie_genres(genre_id))")


with open("gross movies.csv","r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        title = row["Film"].strip().capitalize()

        m_id = db.execute("INSERT INTO movies (title) VALUES(?)", title)
        

        for genre in row["Genre"].split(" , "):
            genre = genre.strip().capitalize()
            genres_id = db.execute("INSERT INTO movie_genres(mg_id) VALUES((SELECT m_id FROM movies WHERE title =?))",title)
            db.execute("INSERT INTO genres (movies_id, genre) VALUES ((SELECT mg_id FROM movie_genres WHERE mg_id=?),?)" , genres_id, genre)