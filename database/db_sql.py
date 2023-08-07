import json
from dataclasses import asdict
import psycopg2
import csv
from config import host, user, password, db_name
from model import Person
from db_factory.nimble_db import NimbleDB


class NimbleDbSQL(NimbleDB):

    def __init__(self, duplication: bool = False):
        self.duplication = duplication
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
        )
        self.connection.autocommit = True

    def create_table(self) -> None:
        with self.connection.cursor() as cursor:
            # Create a table in our database if it doesn't exist
            cursor.execute(
                """CREATE TABLE  IF NOT EXISTS users(
                    id serial PRIMARY KEY,
                    first_name varchar(50),
                    last_name varchar(50),
                    email varchar(50));"""
            )
            # Create an index for full-text search if it doesn't exist
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_users_fulltext_search 
                ON users USING gin(to_tsvector('simple', first_name || ' ' || last_name || ' ' || email));
                """
            )

            print("[INFO] Table created successfully")

    def delete_table(self, table_name: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("""DROP TABLE IF EXISTS users;""")

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

    def insert_value(self, value: Person) -> None:
        with self.connection.cursor() as cursor:
            query = """INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s);"""
            data_to_insert = value.get_fields()
            cursor.execute(query, data_to_insert)

    def update_value(self, exist_value: Person, new_value: Person) -> None:
        with self.connection.cursor() as cursor:
            update_query = f"UPDATE users SET first_name = %s, last_name = %s, email = %s WHERE id = %s"
            data_to_insert = (new_value.first_name, new_value.last_name, new_value.email, exist_value.person_id)
            cursor.execute(update_query, data_to_insert)

    def update_db(self, new_values: dict) -> None:
        for item in new_values['resources']:
            if item['record_type'] == 'person':
                new_person = Person(
                    email=self._get_value(container=item['fields'], param='email'),
                    first_name=self._get_value(container=item['fields'], param='first name'),
                    last_name=self._get_value(container=item['fields'], param='last name'),
                    person_id=None
                )
                if self.duplication:
                    self.insert_value(new_person)
                    continue

                if new_person.email is None:
                    existing_person = self.get_record(full_name=(new_person.first_name, new_person.last_name))

                    if existing_person is not None:
                        if existing_person.email is None:
                            continue
                        else:
                            self.update_value(exist_value=existing_person, new_value=new_person)
                    else:
                        self.insert_value(value=new_person)

                else:
                    existing_person_email = self.get_record(email=new_person.email)
                    if existing_person_email is not None:
                        continue
                    else:
                        existing_person_full_name = self.get_record(
                            full_name=(new_person.first_name, new_person.last_name))
                        if existing_person_full_name is not None:
                            self.update_value(exist_value=existing_person_full_name, new_value=new_person)
                        else:
                            self.insert_value(value=new_person)

    def fulltext_search(self, query: str) -> str:
        """
        :param query:
        :return: JSON
        """
        with self.connection.cursor() as cursor:
            search_query = """
                SELECT COALESCE(first_name, '') as first_name, COALESCE(last_name, '') as last_name, COALESCE(email, '') as email
                FROM users
                WHERE to_tsvector('simple', COALESCE(first_name, '') || ' ' || COALESCE(last_name, '') || ' ' || COALESCE(email, '')) @@ to_tsquery(%s)
            """

            cursor.execute(search_query, (query,))
            results = cursor.fetchall()

            # Converting the results to a list of Person objects
            persons = [Person(*result) for result in results]
        # Converting the results to JSON
        return json.dumps(persons, default=lambda x: asdict(x))

    def get_all_records(self) -> str:
        with self.connection.cursor() as cursor:
            select_query = "SELECT first_name, last_name, email FROM users"
            cursor.execute(select_query)
            results = cursor.fetchall()

        persons = [Person(person_id=row[0], first_name=row[1], last_name=row[2], email=row[3]) for row in results]
        return json.dumps(persons, default=lambda x: asdict(x))

    def get_record(self, id: str = '', email: str = '', full_name: tuple[str, str] | None = None) -> Person | None:
        with self.connection.cursor() as cursor:
            if id:
                select_query = f"SELECT id, first_name, last_name, email FROM users WHERE id = %s"
                cursor.execute(select_query, (id,))
                result = cursor.fetchone()
                return Person(*result) if result else None

            if email:
                select_query = f"SELECT id, first_name, last_name, email FROM users WHERE email = %s"
                cursor.execute(select_query, (email,))
                result = cursor.fetchone()
                return Person(*result) if result else None

            if full_name is not None:
                first_name, last_name = full_name
                query = """
                           SELECT * FROM users
                           WHERE first_name = %s AND last_name = %s;
                        """
                data_to_insert = (first_name, last_name,)
                cursor.execute(query, data_to_insert)
                result = cursor.fetchone()
                return Person(*result) if result else None

    @staticmethod
    def _get_value(container: dict, param: str):
        if param in container.keys():
            value = \
                [i.get('value') if isinstance(i.get('value'), str) else i.get('value')[0] for i in container[param]][0]
            return value.strip() if value else None
        return None

# if __name__ == '__main__':
#     db = NimbleDbSQL(duplication=True)
#     db.create_db()
#     db.update_db_from_csv_file(file_name='../Nimble Contacts.csv')
# db.update_db()

# db.delete_table(table_name='users')
