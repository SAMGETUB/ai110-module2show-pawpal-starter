from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


@dataclass
class Task:
    name: str
    duration: int
    priority: int
    time: datetime
    status: str = "pending"

    def mark_complete(self) -> None:
        self.status = "completed"


@dataclass
class Pet:
    name: str
    species: str
    allergies: List[str] = field(default_factory=list)
    task_list: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.task_list.append(task)

    def get_tasks(self) -> List[Task]:
        return self.task_list


class Owner:
    def __init__(self, name: str, pets_list: Optional[List[Pet]] = None, availability: Optional[str] = None):
        self.name = name
        self.pets_list = pets_list if pets_list is not None else []
        self.availability = availability

    def add_pet(self, pet: Pet) -> None:
        self.pets_list.append(pet)

    def get_pets(self) -> List[Pet]:
        return self.pets_list

    def set_availability(self, availability: str) -> None:
        self.availability = availability


class Scheduler:
    def generate_schedule(self, owner: Owner) -> List[Task]:
        tasks: List[Task] = []
        for pet in owner.get_pets():
            tasks.extend(pet.get_tasks())
        return self.sort_by_time(tasks)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(
        self,
        tasks: List[Task],
        criteria: Optional[Union[Dict[str, Any], Callable[[Task], bool]]] = None,
    ) -> List[Task]:
        if criteria is None:
            return tasks
        if callable(criteria):
            return [task for task in tasks if criteria(task)]
        return [task for task in tasks if all(getattr(task, key, None) == value for key, value in criteria.items())]

    def detect_conflicts(self, tasks: List[Task]) -> List[Tuple[Task, Task]]:
        conflicts: List[Tuple[Task, Task]] = []
        sorted_tasks = self.sort_by_time(tasks)

        for current, next_task in zip(sorted_tasks, sorted_tasks[1:]):
            current_end = current.time + timedelta(minutes=current.duration)
            if current_end > next_task.time:
                conflicts.append((current, next_task))

        return conflicts
