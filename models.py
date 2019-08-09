from get_connection import get_connection, execute_query
from hash_password import password_hash
from time import strftime


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
        create_table_query = """DROP TABLE IF EXISTS Users;
                              CREATE TABLE Users
                              (
                              id                SERIAL PRIMARY KEY,
                              email             VARCHAR(255) UNIQUE,
                              name              VARCHAR(255),
                              hashed_password   VARCHAR(80)
                              );"""

        execute_query(get_connection(), create_table_query)

    @property
    def get_id(self):
        return self.__id

    @property
    def get_password(self):
        return self.__hashed_password

    def set_password(self, password, salt):
        self.__hashed_password = password_hash(password, salt)

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

        elif id is not None or email is not None:
            if id is not None:
                select_query += f" WHERE id = {id};"
            else:
                select_query += f" WHERE email = '{email}';"
            selected = execute_query(get_connection(), select_query, fetch_one=True)
            user = User()
            user.__id = selected[0]
            user.email = selected[1]
            user.name = selected[2]
            user.__hashed_password = selected[3]
            return user

        elif name is not None:
            select_query += f" WHERE name = '{name}';"
            return execute_query(get_connection(), select_query, fetch_all=True)

    def delete(self):

        delete_query = """DELETE FROM Users
                          WHERE id = %s;"""

        execute_query(get_connection(), delete_query, (self.__id, ))
        self.__id = None

    def __str__(self):
        return f'{self.__id, self.email, self.name, self.__hashed_password}'


class Message(object):

    __id = None
    from_id = None
    to_id = None
    text = None
    creation_date = None

    def __init__(self):
        self.__id = None
        self.from_id = None
        self.to_id = None
        self.text = ''
        self.creation_date = strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def create_table():
        create_table_query = """DROP TABLE IF EXISTS Messages;
                              CREATE TABLE Messages
                              (
                              id                SERIAL PRIMARY KEY,
                              from_id           INT REFERENCES Users(id),
                              to_id             INT REFERENCES  Users(id),
                              text              TEXT,
                              creation_date     TIMESTAMP
                              );"""

        execute_query(get_connection(), create_table_query)

    @property
    def get_id(self):
        return self.__id

    def save(self):

        values = (self.from_id, self.to_id, self.text, self.creation_date)

        if self.__id is None:

            insert_query = """INSERT INTO Messages(from_id, to_id, text, creation_date) VALUES 
                              (%s, %s, %s, %s) 
                              RETURNING id;"""

            id_tuple = execute_query(get_connection(), insert_query, values, fetch_one=True)
            self.__id = id_tuple[0]

    @staticmethod
    def load(id=None, from_id=None, to_id=None, text=None, creation_date=None):

        def load_selected(key, value, query, is_where=False):
            if 'id' in key:
                if not is_where:
                    query += f" WHERE {key} = {value}"
                else:
                    query += f" AND {key} = {value}"
                query += ";"
                return query
            else:
                if not is_where:
                    query += f" WHERE {key}::text LIKE '%{value}%';"
                else:
                    query += f" WHERE {key}::text LIKE '%{value}%';"
                query += ";"
                return query

        keys = ['id', 'from_id', 'to_id', 'text', 'creation_date']
        values = [id, from_id, to_id, text, creation_date]
        load_dict = dict(zip(keys, values))

        select_query = """SELECT    *
                          FROM      Messages"""

        none_counter = 0
        for v in values:
            if v is None:
                none_counter += 1

        if none_counter == 5:
            select_query += ";"
            return execute_query(get_connection(), select_query, fetch_all=True)

        elif none_counter <= 4:
            is_where = False
            for k in load_dict:
                if k == 'id' and load_dict[k] is not None:
                    select_query = load_selected(k, load_dict[k], select_query)
                    selected = execute_query(get_connection(), select_query, fetch_one=True)
                    message = Message()
                    message.__id = selected[0]
                    message.from_id = selected[1]
                    message.to_id = selected[2]
                    message.text = selected[3]
                    message.creation_date = selected[4]
                    return message
                elif k != 'id' and load_dict[k] is not None:
                    if not is_where:
                        select_query = load_selected(k, load_dict[k], select_query)
                        is_where = True
                    else:
                        select_query = load_selected(k, load_dict[k], select_query, is_where=True)

        return execute_query(get_connection(), select_query, fetch_all=True)

    def delete(self):

        delete_query = """DELETE FROM Messages
                          WHERE id = %s;"""

        execute_query(get_connection(), delete_query, (self.__id, ))
        self.__id = None

    def __str__(self):
        return f'{self.__id, self.from_id, self.to_id, self.text, self.creation_date}'


if __name__ == '__main__':

    m = Message().load(text='w')
    print(m)