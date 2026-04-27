# Oscar Avina
# 04/26/2026
# Module 6.2 Assignment

""" import statements """
import mysql.connector  # to connect
from mysql.connector import errorcode

import dotenv  # to use .env file
from dotenv import dotenv_values


# using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True,
    "ssl_disabled": True
}

try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database

    cursor = db.cursor()

    # Query 1: Select all fields from the studio table
    print("-- DISPLAYING Studio RECORDS --")

    cursor.execute("SELECT * FROM studio")

    studios = cursor.fetchall()

    for studio in studios:
        print("Studio ID: {}".format(studio[0]))
        print("Studio Name: {}\n".format(studio[1]))

    # Query 2: Select all fields from the genre table
    print("-- DISPLAYING Genre RECORDS --")

    cursor.execute("SELECT * FROM genre")

    genres = cursor.fetchall()

    for genre in genres:
        print("Genre ID: {}".format(genre[0]))
        print("Genre Name: {}\n".format(genre[1]))

    # Query 3: Select movie names and runtimes for movies under two hours
    print("-- DISPLAYING Short Film RECORDS --")

    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")

    films = cursor.fetchall()

    for film in films:
        print("Film Name: {}".format(film[0]))
        print("Runtime: {}\n".format(film[1]))

    # Query 4: Select film names and directors ordered by director
    print("-- DISPLAYING Director RECORDS in Order --")

    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director, film_name DESC")

    directors = cursor.fetchall()

    for director in directors:
        print("Film Name: {}".format(director[0]))
        print("Director: {}\n".format(director[1]))

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """

    db.close()