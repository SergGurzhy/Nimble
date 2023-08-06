import csv
from dataclasses import asdict

from db_factory.nimble_db import NimbleDB
from model import Person


class MokeDB(NimbleDB):

    def __init__(self, duplication: bool = False):
        self.duplication = duplication
        self.create_table()
        self.update_db_from_csv_file(file_name=r'D:\Поиск работы\Nimble\Nimble\tests\test_contacts.csv')

    def create_table(self) -> None:
        setattr(self, "storage", [])

    def delete_table(self, table_name: str) -> None:
        if hasattr(self, 'storage'):
            del self.storage

    def update_db_from_csv_file(self, file_name: str) -> None:
        with open(file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.storage.append(
                    {
                        'first_name': row['first name'],
                        'last_name': row['last name'],
                        'email': row['Email']
                    }
                )

    def insert_value(self, values: Person) -> None:
        self.storage.append(asdict(values))

    def update_value(self, values: Person) -> None:
        # TODO If no email field????
        for record in self.storage:
            if record['email'] == values.email:
                record['first_name'] = values.first_name
                record['last_name'] = values.last_name
                break

    def update_db(self, new_values: dict) -> None:
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
        results = [rec for rec in self.storage if query.lower() in ' '.join(rec.values()).lower()]
        return [Person(**record) for record in results]

    def get_all_records(self) -> list[Person]:
        return [Person(**rec) for rec in self.storage]

    def _email_in_db(self, email: str) -> Person | None:
        for record in self.storage:
            if email in [item for item in record.values]:
                return Person(**record)
        return None

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


if __name__ == '__main__':
    db = MokeDB(duplication=True)
    pass

#     db.create_db()
#     db.update_db_from_csv_file(file_name='../Nimble Contacts.csv')
    # db.update_db()

    # db.delete_table(table_name='users')