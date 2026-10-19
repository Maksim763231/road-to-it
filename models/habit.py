from dataclasses import dataclass

@dataclass
class Habit:
    id: int | None
    chat_id: int
    title: str
    active: bool = True