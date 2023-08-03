from dataclasses import dataclass, asdict


@dataclass
class Person:
    first_name: str
    last_name: str
    email: str

    def get_fields(self) -> tuple:
        person_dict: dict[str] = asdict(self)
        return tuple(person_dict.values())
