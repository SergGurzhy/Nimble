import json
import psycopg2
import csv
from config import host, user, password, db_name
from nimble_db import NimbleDB


class NimbleDbSQL(NimbleDB):
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.connection.autocommit = True

    def create_db(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE  IF NOT EXISTS users(
                    id serial PRIMARY KEY,
                    first_name varchar(50),
                    last_name varchar(50),
                    email varchar(50));"""
            )

            print("[INFO] Table created successfully")

    def update_db_from_csv_file(self, file_name: str) -> None:
        with open(file_name, 'r') as csv_file:
            with self.connection.cursor() as cursor:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)

                for row in csv_reader:
                    query = f"INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)"
                    first_name, last_name, email = row
                    data = (first_name, last_name, email)
                    cursor.execute(query, data)

    def insert_value(self, values: tuple[str, str, str]) -> None:
        first_name, last_name, email = values
        with self.connection.cursor() as cursor:
            query = """INSERT INTO users (email, first_name, last_name) VALUES (%s, %s, %s);"""
            data_to_insert = (first_name, last_name, email)
            cursor.execute(query, data_to_insert)

    def update_value(self, value: tuple[str, str], key: str) -> None:
        first_name, last_name = value
        email = key
        with self.connection.cursor() as cursor:
            update_query = f"UPDATE users SET first_name = %s, last_name = %s WHERE email = %s"
            data_to_insert = (first_name, last_name, email)
            cursor.execute(update_query, data_to_insert)

    def update_db(self) -> None:
        with open("response.json") as file:
            data_file = json.load(file)

        for item in data_file['resources']:
            if item['record_type'] == 'person':
                email = self._get_value(container=item['fields'], param='email')
                if self._email_in_db(email=email):
                    continue
                else:
                    first_name = self._get_value(container=item['fields'], param='first name')
                    last_name = self._get_value(container=item['fields'], param='last name')
                self.insert_value(values=(first_name, last_name, email))

                # with self.connection.cursor() as cursor:
                #     query = """INSERT INTO users (email, first_name, last_name) VALUES (%s, %s, %s);"""
                #     data_to_update = (first_name, last_name, email)
                #     cursor.execute(query, data_to_update)

    def _email_in_db(self, email: str) -> bool:
        with self.connection.cursor() as cursor:
            select_query = f"SELECT COUNT(*) FROM users WHERE email = %s"
            cursor.execute(select_query, email)
            return len(cursor.fetchone()[0]) > 0

    @staticmethod
    def _get_value(container: dict, param: str):
        if param in container.keys():
            value = [i.get('value') if isinstance(i.get('value'), str) else i.get('value')[0] for i in container[param]][0]
            return value.strip() if value else None
        return None


if __name__ == '__main__':
    db = NimbleDbSQL()
    db.create_db()
    db.update_db_from_csv_file(file_name='Nimble Contacts.csv')
    db.update_db()

# try:
#     # connect to exist database
#     connection = psycopg2.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=db_name
#     )
#     connection.autocommit = True
#
#     # the cursor for perfoming database operations
#     # cursor = connection.cursor()
#
#     # with connection.cursor() as cursor:
#     #     cursor.execute(
#     #         "SELECT version();"
#     #     )
#     #
#     #     print(f"Server version: {cursor.fetchone()}")
#
#     # create a new table
#     with connection.cursor() as cursor:
#         cursor.execute(
#             """CREATE TABLE  IF NOT EXISTS users(
#                 id serial PRIMARY KEY,
#                 first_name varchar(50) NOT NULL,
#                 last_name varchar(50) NOT NULL,
#                 email varchar(50) NOT NULL);"""
#         )
#
#         # connection.commit()
#         print("[INFO] Table created successfully")

# insert data into a table
# with connection.cursor() as cursor:
#     cursor.execute(
#         """INSERT INTO users (first_name, nick_name) VALUES
#         ('Oleg', 'barracuda');"""
#     )

#     print("[INFO] Data was succefully inserted")

# get data from a table
# with connection.cursor() as cursor:
#     cursor.execute(
#         """SELECT nick_name FROM users WHERE first_name = 'Oleg';"""
#     )

#     print(cursor.fetchone())

# delete a table
# with connection.cursor() as cursor:
#     cursor.execute(
#         """DROP TABLE users;"""
#     )

#     print("[INFO] Table was deleted")

# except Exception as _ex:
#     print("[INFO] Error while working with PostgreSQL", _ex)
