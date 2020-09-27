import psycopg2
from functools import wraps

def db_connect(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        db_connection = psycopg2.connect(database='jobsitychatdb')
        db_cursor = db_connection.cursor()
        db_connection.rollback()
        return f(db_cursor, db_connection, *args, **kwargs)
    return decorated
