from psycopg2 import connect, DatabaseError
from connection_info import connection_info


def get_connection():
    try:
        conn = connect(**connection_info)
        return conn

    except DatabaseError as error:
        print(error)


def execute_query(conn, sql_query, values=(), fetch_one=False, fetch_all=False):

    try:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql_query, values)
        if fetch_one:
            return cur.fetchone()
        if fetch_all:
            return cur.fetchall()

    except DatabaseError as error:
        print(error)

    else:
        cur.close()

    finally:
        conn.close()
