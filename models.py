from get_connection import get_connection, execute_query


class User(object):

    __id = None
    name = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = None
        self.name = ''
        self.email = ''
        self.__hashed_password = ''

    @staticmethod
    def create_table():
        sql_create_table = """DROP TABLE IF EXISTS Users;
                              CREATE TABLE Users
                              (
                              id                SERIAL PRIMARY KEY,
                              email             VARCHAR(255) UNIQUE,
                              name              VARCHAR(255),
                              hashed_password   VARCHAR(80)
                              );"""

        execute_query(get_connection(), sql_create_table)

    @property
    def get_id(self):
        return self.__id

    @property
    def get_password(self):
        return self.__hashed_password

    # def set_password(self, password, salt):
    #     self.__hashed_password = password_hash(password, salt)

    def save(self):

        values = (self.email, self.name, self.__hashed_password)

        if self.__id is None:

            insert_query = """INSERT INTO Users(email, name, hashed_password) VALUES (%s, %s, %s) RETURNING id;"""

            id_tuple = execute_query(get_connection(), insert_query, values, fetch_one=True)
            self.__id = id_tuple[0]

        else:

            update_query = """UPDATE Users
                              SET    email = %s,
                                     name = %s,
                                     hashed_password = %s
                              WHERE  id = %s;"""

            values += (self.__id, )

            execute_query(get_connection(), update_query, values)

    @staticmethod
    def load(id=None, email=None, name=None):

        select_query = """SELECT    *
                          FROM      Users"""

        if id is None and email is None and name is None:
            select_query += ";"
            return execute_query(get_connection(), select_query, fetch_all=True)

        if id is not None or email is not None:
            if id is not None:
                select_query += f" WHERE id = '{id}';"
            else:
                select_query += f" WHERE email = '{email}';"
            selected = execute_query(get_connection(), select_query, fetch_one=True)
            user = User()
            user.__id = selected[0]
            user.email = selected[1]
            user.name = selected[2]
            user.__hashed_password = selected[3]
            return user

        if name is not None:
            select_query += f" WHERE name = '{name}';"
            return execute_query(get_connection(), select_query, fetch_all=True)

    def delete(self):

        delete_query = """DELETE FROM Users
                          WHERE id = %s;"""

        execute_query(get_connection(), delete_query, (self.__id, ))
        self.__id = None

    def __str__(self):
        return f'{self.__id, self.email, self.name, self.__hashed_password}'


if __name__ == '__main__':

    u = User().load(email='andrzej2@andrzej.com')
    u.delete()