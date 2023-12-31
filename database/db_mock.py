import csv
import json
import os
from dataclasses import asdict

from db_factory.nimble_db import NimbleDB
from server_helpers.models.person import Person

INITIALIZE_DATA = 'test_data/test_contacts.csv'


class MockDB(NimbleDB):

    def __init__(self, duplication: bool = False):
        self.duplication = duplication
        self.storage = []

    def initialization_db(self, table_name: str):
        self.update_db_from_csv_file(file_name=INITIALIZE_DATA)

    def create_table(self, table_name: str) -> None:
        setattr(self, "storage", [])

    def delete_table(self, table_name: str) -> None:
        if hasattr(self, table_name):
            del self.storage

    def update_db_from_csv_file(self, file_name: str) -> None:
        def get_value(data: str) -> str | None:
            return data if len(data) > 0 else None

        path = os.path.join(os.getcwd(), file_name)
        count = 1
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.storage.append(
                    {
                        'person_id': str(count),
                        'first_name': get_value(row['first name']),
                        'last_name': get_value(row['last name']),
                        'email': get_value(row['email']),
                        'description': get_value(row['description'])
                    }
                )
                count += 1

    def insert_value(self, value: Person) -> None:
        self.storage.append(asdict(value))

    def update_value(self, exist_value: Person, new_value: Person) -> None:
        # Update record. 'person_id' remains the same
        for attr, value in new_value.__dict__.items():
            if attr != 'person_id':
                setattr(exist_value, attr, value)

        # save in database
        self.storage[int(exist_value.person_id) - 1] = asdict(exist_value)

    def get_record(self, person_id: str = '', email: str = '', full_name: tuple[str, str] | None = None) -> Person | None:

        if person_id:
            result = [rec for rec in self.storage if rec.get('person_id') == person_id]
            return Person(**result[0]) if len(result) > 0 else None
        if email:
            result = [rec for rec in self.storage if rec.get('email') == email]
            return Person(**result[0]) if len(result) > 0 else None

        if full_name is not None:
            first_name, last_name = full_name
            result = []
            for rec in self.storage:
                if first_name == rec['first_name'] and last_name == rec['last_name']:
                    result.append(rec)
            return Person(**result[0]) if len(result) > 0 else None

    def update_db(self, new_values: dict) -> dict[str]:
        count_insert = 0
        count_update = 0
        for item in new_values['resources']:
            if item['record_type'] == 'person':
                new_person = Person(
                    email=self._get_value(container=item['fields'], param='email'),
                    first_name=self._get_value(container=item['fields'], param='first name'),
                    last_name=self._get_value(container=item['fields'], param='last name'),
                    person_id=str(len(self.storage) + 1),
                    description=self._get_value(container=item['fields'], param='description')
                )
                if self.duplication:
                    self.insert_value(new_person)
                    count_insert += 1
                    continue

                if new_person.email is None:
                    existing_person = self.get_record(full_name=(new_person.first_name, new_person.last_name))

                    if existing_person is not None:
                        if existing_person.email is None:
                            continue
                        else:
                            self.update_value(exist_value=existing_person, new_value=new_person)
                            count_update += 1
                    else:
                        self.insert_value(value=new_person)
                        count_insert += 1
                else:
                    existing_person_email = self.get_record(email=new_person.email)
                    if existing_person_email is not None:
                        continue
                    else:
                        existing_person_full_name = self.get_record(full_name=(new_person.first_name, new_person.last_name))
                        if existing_person_full_name is not None:
                            self.update_value(exist_value=existing_person_full_name, new_value=new_person)
                            count_update += 1
                        else:
                            self.insert_value(value=new_person)
                            count_insert += 1
        return {'count_insert': str(count_insert), 'count_update': str(count_update)}

    def fulltext_search(self, query: str) -> str:
        results = [rec for rec in self.storage if query.lower() in ' '.join(rec.values()).lower()]
        persons = [Person(**record) for record in results]
        return json.dumps(persons, default=lambda x: asdict(x))

    def get_all_entries(self) -> str:
        persons = [Person(**rec) for rec in self.storage]
        return json.dumps(persons, default=lambda x: asdict(x))

    def _email_in_db(self, email: str) -> Person | None:
        for record in self.storage:
            if email in [item for item in record.values()]:
                return Person(**record)
        return None

    @staticmethod
    def _get_value(container: dict, param: str):
        if param in container.keys():
            values = [i.get('value') for i in container[param]]
            return values[0].strip() if values else None
        return None

    @staticmethod
    def _changed_first_and_last_name(new_person: Person, existing_person: Person) -> bool:
        """
        Checks if fields first_name or last_name have been changed.
        Return:  True if changed
        """
        return new_person == existing_person
