from psycopg2 import connect, DatabaseError
from connection_info import connection_info


def create_database():

    drop_db_query = """DROP DATABASE IF EXISTS message_app_db;"""

    create_db_query = """CREATE DATABASE message_app_db
                         ENCODING 'UTF-8';"""

    create_database_info = {key: connection_info[key] for key in connection_info if key != 'database'}

    try:
        conn = connect(**create_database_info)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(drop_db_query)
        cur.execute(create_db_query)

        cur.close()
        conn.close()

    except DatabaseError as error:
        print(error)


if __name__ == '__main__':
    create_database()
