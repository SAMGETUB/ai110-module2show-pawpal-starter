from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    name: str
    duration: int
    priority: int
    time: datetime
    status: str

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    allergies: List[str] = field(default_factory=list)
    task_list: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(self, name: str, pets_list: Optional[List[Pet]] = None, availability: Optional[str] = None):
        self.name = name
        self.pets_list = pets_list if pets_list is not None else []
        self.availability = availability

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        pass

    def set_availability(self, availability: str) -> None:
        pass


class Scheduler:
    def generate_schedule(self, owner: Owner):
        pass

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        pass

    def filter_tasks(self, tasks: List[Task], criteria):
        pass

    def detect_conflicts(self, tasks: List[Task]):
        pass
