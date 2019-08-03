# from psycopg2 import connect, DatabaseError
# from connection_info import connection_info
from models import User


def create_tables():

    for cls in [User]:
        cls.create_table()


if __name__ == '__main__':
    create_tables()
