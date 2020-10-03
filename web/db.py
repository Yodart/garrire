import psycopg2
from functools import wraps

# Wrapper to make a connection to the database. Designed to be used
# throughout the endpoints to get access to the psycopg2 cursor and
# connection to then interact with the database.

def db_connect(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        db_connection = psycopg2.connect(database='jobsitychatdb',
                                         user = "jobsity",
                                         password = "jobsity",
                                         host='db',
                                         port = "5432",)
        db_cursor = db_connection.cursor()
        db_connection.rollback()
        return f(db_cursor, db_connection, *args, **kwargs)
    return decorated
