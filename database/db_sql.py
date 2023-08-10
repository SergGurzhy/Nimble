import json
import os
import sys
from dataclasses import asdict
import psycopg2
import csv
from dotenv import load_dotenv
from server_helpers.models.db_env import DBEnv
from server_helpers.models.person import Person
from db_factory.nimble_db import NimbleDB
from psycopg2.extensions import AsIs

load_dotenv(sys.path[0] + '.env')

TABLE_NAME = 'users'
START_DATA = 'Nimble Contacts.csv'


def get_environment_variables() -> DBEnv:
    return DBEnv(
        db_name=os.getenv('POSTGRES_DB'),
        host=os.getenv('POSTGRES_HOST'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv('POSTGRES_PORT')
    )


class NimbleDbSQL(NimbleDB):

    def __init__(self, duplication: bool = False):
        self.env = get_environment_variables()
        self.duplication = duplication
        self.connection = psycopg2.connect(
            host=self.env.host,
            user=self.env.user,
            password=self.env.password,
            database=self.env.db_name,
        )
        self.connection.autocommit = True
        self.initialization_db(table_name=TABLE_NAME)

    def _table_exists(self, table_name: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table_name,))
        return cursor.fetchone()[0]

    def _count_entries(self, table_name: str) -> int:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        return cursor.fetchone()[0]

    def initialization_db(self, table_name: str) -> None:
        if not self._table_exists(table_name):
            self.create_table(table_name=TABLE_NAME)

        if self._count_entries(table_name=TABLE_NAME) == 0:
            path = os.path.join(os.getcwd(), START_DATA)
            self.update_db_from_csv_file(file_name=path)

        count_entries = self._count_entries(table_name=TABLE_NAME)
        print(f"[INFO] Database connection completed successfully. Loaded data: {count_entries} ")

    def create_table(self, table_name: str = '') -> None:
        with self.connection.cursor() as cursor:
            # Create a table in our database if it doesn't exist
            create_table_query = """
                        CREATE TABLE IF NOT EXISTS %s (
                            id serial PRIMARY KEY,
                            first_name varchar(50),
                            last_name varchar(50),
                            email varchar(50)
                        );
                    """
            cursor.execute(create_table_query, (AsIs(table_name),))

            # Create an index for full-text search if it doesn't exist
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_users_fulltext_search 
                ON users USING gin(to_tsvector('simple', first_name || ' ' || last_name || ' ' || email));
                """
            )

    def delete_table(self, table_name: str = TABLE_NAME) -> None:
        with self.connection.cursor() as cursor:
            query = "DROP TABLE IF EXISTS %s;"
            cursor.execute(query, (AsIs(table_name),))

    def update_db_from_csv_file(self, file_name: str = '') -> None:
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
            data_to_insert = value.get_fields()[1:] # Delete id==none
            print(f'db_sql.py:  data_to_insert = {data_to_insert}')
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
                        SELECT id, COALESCE(first_name, '') as first_name, COALESCE(last_name, '') as last_name, COALESCE(email, '') as email
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
            select_query = "SELECT id, first_name, last_name, email FROM users"
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
