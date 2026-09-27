from dataclasses import dataclass

@dataclass
class User:
    chat_id: int
    username: str
    time: str
    enabled: bool
    timezone: str

User(
    chat_id=1784197771,
    username="maksim",
    time="08:00",
    enabled=True,
    timezone="Moscow/Europe"
)