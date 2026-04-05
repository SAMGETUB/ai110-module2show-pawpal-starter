from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Avery")

    cat = Pet(name="Milo", species="Cat", allergies=["pollen"])
    dog = Pet(name="Scout", species="Dog", allergies=["wheat"])

    owner.add_pet(cat)
    owner.add_pet(dog)

    cat.add_task(Task(name="Feed Milo", duration=15, priority=1, time=datetime(2026, 4, 5, 8, 0)))
    cat.add_task(Task(name="Give Milo medication", duration=10, priority=2, time=datetime(2026, 4, 5, 9, 30)))
    dog.add_task(Task(name="Walk Scout", duration=30, priority=1, time=datetime(2026, 4, 5, 7, 30)))

    scheduler = Scheduler()
    tasks = scheduler.generate_schedule(owner)

    print("Today's Schedule")
    print("---------------")
    for task in tasks:
        print(f"{task.time.strftime('%H:%M')} - {task.name} ({task.status})")


if __name__ == "__main__":
    main()
