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
    pet_name: Optional[str] = None
    recurrence: Optional[str] = None

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.status = "completed"


@dataclass
class Pet:
    name: str
    species: str
    allergies: List[str] = field(default_factory=list)
    task_list: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        task.pet_name = self.name
        self.task_list.append(task)

    def get_tasks(self) -> List[Task]:
        """Return this pet's current tasks."""
        return self.task_list


class Owner:
    def __init__(self, name: str, pets_list: Optional[List[Pet]] = None, availability: Optional[str] = None):
        self.name = name
        self.pets_list = pets_list if pets_list is not None else []
        self.availability = availability

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets_list.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return the owner's pets."""
        return self.pets_list

    def set_availability(self, availability: str) -> None:
        """Set the owner's availability."""
        self.availability = availability


class Scheduler:
    def generate_schedule(self, owner: Owner) -> List[Task]:
        """Generate a sorted schedule of tasks for the owner."""
        tasks: List[Task] = []
        for pet in owner.get_pets():
            tasks.extend(pet.get_tasks())
        return self.sort_by_time(tasks)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their scheduled time, then by priority (lower priority number first)."""
        return sorted(tasks, key=lambda task: (task.time, task.priority))

    def filter_tasks(
        self,
        tasks: List[Task],
        criteria: Optional[Union[Dict[str, Any], Callable[[Task], bool]]] = None,
    ) -> List[Task]:
        """Filter tasks by a criteria or callback."""
        if criteria is None:
            return tasks
        if callable(criteria):
            return [task for task in tasks if criteria(task)]
        return [task for task in tasks if all(getattr(task, key, None) == value for key, value in criteria.items())]

    def filter_by_status(self, tasks: List[Task], status: str) -> List[Task]:
        """Filter tasks by status."""
        return [task for task in tasks if task.status == status]

    def filter_by_pet(self, tasks: List[Task], pet_name: str) -> List[Task]:
        """Filter tasks by pet name."""
        return [task for task in tasks if task.pet_name == pet_name]

    def detect_conflicts(self, tasks: List[Task]) -> List[Tuple[Task, Task]]:
        """Detect overlapping tasks in the provided task list."""
        conflicts: List[Tuple[Task, Task]] = []
        sorted_tasks = self.sort_by_time(tasks)

        for current, next_task in zip(sorted_tasks, sorted_tasks[1:]):
            current_end = current.time + timedelta(minutes=current.duration)
            if current_end > next_task.time:
                conflicts.append((current, next_task))

        return conflicts

    def generate_recurring_tasks(self, task: Task, num_days: int) -> List[Task]:
        """Generate recurring task instances for the next num_days days."""
        if not task.recurrence:
            return [task]
        
        tasks = []
        delta = timedelta(days=1) if task.recurrence == "daily" else timedelta(days=7)
        
        for i in range(num_days):
            new_time = task.time + i * delta
            new_task = Task(
                name=task.name,
                duration=task.duration,
                priority=task.priority,
                time=new_time,
                status=task.status,
                pet_name=task.pet_name,
                recurrence=task.recurrence
            )
            tasks.append(new_task)
        
        return tasks
