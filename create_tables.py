from models import User, Message


def create_tables():

    for cls in [Message]:
        cls.create_table()


if __name__ == '__main__':
    create_tables()
