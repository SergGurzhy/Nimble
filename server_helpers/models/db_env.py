from dataclasses import dataclass


@dataclass
class DBEnv:
    db_name: str
    host: str
    user: str
    password: str
