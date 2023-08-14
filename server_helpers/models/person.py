from dataclasses import dataclass, asdict


@dataclass
class Person:
    person_id: str | None
    first_name: str
    last_name: str
    email: str
    description: str

    def __dict__(self):
        return asdict(self)

    def get_fields(self) -> tuple:
        person_dict: dict[str] = asdict(self)
        return tuple(person_dict.values())
