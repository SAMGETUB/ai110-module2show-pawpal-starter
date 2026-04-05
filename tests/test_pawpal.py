from datetime import datetime

from pawpal_system import Pet, Task


def test_task_mark_complete_updates_status() -> None:
    task = Task(name="Feed pet", duration=10, priority=1, time=datetime.now())

    task.mark_complete()

    assert task.status == "completed"


def test_pet_add_task_increases_task_count() -> None:
    pet = Pet(name="Milo", species="Cat")
    initial_count = len(pet.get_tasks())
    task = Task(name="Groom pet", duration=20, priority=2, time=datetime.now())

    pet.add_task(task)

    assert len(pet.get_tasks()) == initial_count + 1
