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

    def insert_value(self, values: Person) -> None:
        with self.connection.cursor() as cursor:
            query = """INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s);"""
            data_to_insert = values.get_fields()
            cursor.execute(query, data_to_insert)

    def update_value(self, values: Person) -> None:
        with self.connection.cursor() as cursor:
            update_query = f"UPDATE users SET first_name = %s, last_name = %s WHERE email = %s"
            data_to_insert = values.get_fields()
            cursor.execute(update_query, data_to_insert)

    def update_db(self, new_values: dict) -> None:
        # with open("response.json") as file:
        #     data_file = json.load(file)

        for item in new_values['resources']:
            if item['record_type'] == 'person':
                new_person = Person(
                    email=self._get_value(container=item['fields'], param='email'),
                    first_name=self._get_value(container=item['fields'], param='first name'),
                    last_name=self._get_value(container=item['fields'], param='last name'),
                )
                if self.duplication:
                    self.insert_value(new_person)
                    continue

                existing_person = self._email_in_db(email=new_person.email)
                if existing_person is not None:
                    if self._changed_first_and_last_name(new_person=new_person, existing_person=existing_person):
                        self.update_value(values=new_person)
                    else:
                        continue
                else:
                    self.insert_value(values=new_person)

    def fulltext_search(self, query: str) -> list[Person]:
        """
        Полнотекстовый поиск по всем полям в таблице users.
        Возвращает список объектов Person, удовлетворяющих условиям поиска.
        """
        print('ЗАШЛИ В МЕТОД SEARCH')
        with self.connection.cursor() as cursor:
            search_query = """
                SELECT COALESCE(first_name, '') as first_name, COALESCE(last_name, '') as last_name, COALESCE(email, '') as email
                FROM users
                WHERE to_tsvector('simple', COALESCE(first_name, '') || ' ' || COALESCE(last_name, '') || ' ' || COALESCE(email, '')) @@ to_tsquery(%s)
            """

            cursor.execute(search_query, (query,))
            results = cursor.fetchall()
            print(f'RESULT: {results}')
            # Преобразование результатов в список объектов Person
            persons = [Person(*result) for result in results]

        return persons

    def get_all_records(self) -> list[Person]:
        with self.connection.cursor() as cursor:
            select_query = "SELECT first_name, last_name, email FROM users"
            cursor.execute(select_query)
            results = cursor.fetchall()

        persons = [Person(first_name=row[0], last_name=row[1], email=row[2]) for row in results]
        return persons

    def _email_in_db(self, email: str) -> Person | None:
        """ Checking availability by field: Email """
        with self.connection.cursor() as cursor:
            select_query = f"SELECT first_name, last_name, email FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            result = cursor.fetchone()
            print(result)
            return Person(*result) if result else None

    @staticmethod
    def _get_value(container: dict, param: str):
        if param in container.keys():
            value = \
                [i.get('value') if isinstance(i.get('value'), str) else i.get('value')[0] for i in container[param]][0]
            return value.strip() if value else None
        return None

    @staticmethod
    def _changed_first_and_last_name(new_person: Person, existing_person: Person) -> bool:
        """
        Checks if fields first_name or last_name have been changed.
        Return:  True if changed
        """
        return new_person == existing_person


# if __name__ == '__main__':
#     db = NimbleDbSQL(duplication=True)
#     db.create_db()
#     db.update_db_from_csv_file(file_name='../Nimble Contacts.csv')
    # db.update_db()

    # db.delete_table(table_name='users')
