from db_factory.nimble_db import NimbleDB
from model import Person


class MokeDB(NimbleDB):

    def __init__(self, duplication: bool = False):
        pass

    def create_db(self) -> None:
        pass

    def delete_table(self, table_name: str) -> None:
        pass

    def update_db_from_csv_file(self, file_name: str) -> None:
        # with open(file_name, 'r') as csv_file:
        pass

    def insert_value(self, values: Person) -> None:
        pass

    def update_value(self, values: Person) -> None:
        pass

    def update_db(self, new_value) -> None:
        pass
        # with open("response.json") as file:
        #     data_file = json.load(file)

        # for item in new_value['resources']:
        #     if item['record_type'] == 'person':
        #         new_person = Person(
        #             email=self._get_value(container=item['fields'], param='email'),
        #             first_name=self._get_value(container=item['fields'], param='first name'),
        #             last_name=self._get_value(container=item['fields'], param='last name'),
        #         )
        #         if self.duplication:
        #             self.insert_value(new_person)
        #             continue
        #
        #         existing_person = self._email_in_db(email=new_person.email)
        #         if existing_person is not None:
        #             if self._changed_first_and_last_name(new_person=new_person, existing_person=existing_person):
        #                 self.update_value(values=new_person)
        #             else:
        #                 continue
        #         else:
        #             self.insert_value(values=new_person)

    def fulltext_search(self, query: str) -> list[Person]:
      pass

    def get_all_records(self) -> list[Person]:
        pass

    def _email_in_db(self, email: str) -> Person | None:
        pass

    @staticmethod
    def _get_value(container: dict, param: str):
        pass
        # if param in container.keys():
        #     value = \
        #         [i.get('value') if isinstance(i.get('value'), str) else i.get('value')[0] for i in container[param]][0]
        #     return value.strip() if value else None
        # return None

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