from datetime import datetime, timedelta

from pawpal_system import Pet, Scheduler, Task


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


def test_scheduler_sort_by_time_with_priority() -> None:
    scheduler = Scheduler()
    time = datetime(2026, 4, 5, 8, 0)
    task1 = Task(name="High priority", duration=10, priority=1, time=time)
    task2 = Task(name="Low priority", duration=10, priority=3, time=time)
    task3 = Task(name="Medium priority", duration=10, priority=2, time=time)
    tasks = [task2, task1, task3]  # Unsorted order

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert sorted_tasks[0].name == "High priority"
    assert sorted_tasks[1].name == "Medium priority"
    assert sorted_tasks[2].name == "Low priority"


def test_scheduler_sort_two_tasks_same_time_by_priority() -> None:
    scheduler = Scheduler()
    time = datetime(2026, 4, 5, 9, 0)
    low_priority_task = Task(name="Low priority", duration=10, priority=3, time=time)
    high_priority_task = Task(name="High priority", duration=10, priority=1, time=time)

    sorted_tasks = scheduler.sort_by_time([low_priority_task, high_priority_task])

    assert sorted_tasks[0] is high_priority_task
    assert sorted_tasks[1] is low_priority_task


def test_scheduler_daily_recurrence_after_completion() -> None:
    scheduler = Scheduler()
    base_time = datetime(2026, 4, 5, 8, 0)
    task = Task(name="Daily meds", duration=10, priority=1, time=base_time, recurrence="daily")

    task.mark_complete()
    recurring_tasks = scheduler.generate_recurring_tasks(task, 2)

    assert task.status == "completed"
    assert recurring_tasks[0].time == base_time
    assert recurring_tasks[1].time == base_time + timedelta(days=1)
    assert recurring_tasks[0].status == "completed"
    assert recurring_tasks[1].status == "completed"


def test_scheduler_detects_conflict_for_same_time_tasks() -> None:
    scheduler = Scheduler()
    time = datetime(2026, 4, 5, 8, 0)
    task1 = Task(name="Task 1", duration=10, priority=1, time=time)
    task2 = Task(name="Task 2", duration=15, priority=2, time=time)

    conflicts = scheduler.detect_conflicts([task1, task2])

    assert len(conflicts) == 1
    assert conflicts[0] == (task1, task2)


def test_scheduler_filter_by_status() -> None:
    scheduler = Scheduler()
    task1 = Task(name="Task 1", duration=10, priority=1, time=datetime.now(), status="pending")
    task2 = Task(name="Task 2", duration=10, priority=1, time=datetime.now(), status="completed")
    task3 = Task(name="Task 3", duration=10, priority=1, time=datetime.now(), status="pending")
    tasks = [task1, task2, task3]

    filtered = scheduler.filter_by_status(tasks, "pending")

    assert len(filtered) == 2
    assert all(task.status == "pending" for task in filtered)


def test_scheduler_filter_by_pet() -> None:
    scheduler = Scheduler()
    task1 = Task(name="Task 1", duration=10, priority=1, time=datetime.now(), pet_name="Milo")
    task2 = Task(name="Task 2", duration=10, priority=1, time=datetime.now(), pet_name="Scout")
    task3 = Task(name="Task 3", duration=10, priority=1, time=datetime.now(), pet_name="Milo")
    tasks = [task1, task2, task3]

    filtered = scheduler.filter_by_pet(tasks, "Milo")

    assert len(filtered) == 2
    assert all(task.pet_name == "Milo" for task in filtered)


def test_scheduler_generate_recurring_tasks_daily() -> None:
    scheduler = Scheduler()
    base_time = datetime(2026, 4, 5, 8, 0)
    task = Task(name="Daily walk", duration=30, priority=1, time=base_time, recurrence="daily")
    
    recurring_tasks = scheduler.generate_recurring_tasks(task, 3)
    
    assert len(recurring_tasks) == 3
    assert recurring_tasks[0].time == base_time
    assert recurring_tasks[1].time == base_time + timedelta(days=1)
    assert recurring_tasks[2].time == base_time + timedelta(days=2)
    assert all(t.recurrence == "daily" for t in recurring_tasks)


def test_scheduler_generate_recurring_tasks_weekly() -> None:
    scheduler = Scheduler()
    base_time = datetime(2026, 4, 5, 8, 0)
    task = Task(name="Weekly grooming", duration=60, priority=2, time=base_time, recurrence="weekly")
    
    recurring_tasks = scheduler.generate_recurring_tasks(task, 2)
    
    assert len(recurring_tasks) == 2
    assert recurring_tasks[0].time == base_time
    assert recurring_tasks[1].time == base_time + timedelta(days=7)
    assert all(t.recurrence == "weekly" for t in recurring_tasks)


def test_scheduler_generate_recurring_tasks_no_recurrence() -> None:
    scheduler = Scheduler()
    task = Task(name="One-time task", duration=10, priority=1, time=datetime.now())
    
    recurring_tasks = scheduler.generate_recurring_tasks(task, 5)
    
    assert len(recurring_tasks) == 1
    assert recurring_tasks[0] == task
