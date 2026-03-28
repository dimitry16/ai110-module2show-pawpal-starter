import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler


# ── Helpers ────────────────────────────────────────────────────────────────

def make_owner(*pets, start=480, end=600):
    """Return an Owner with the given pets and an available window."""
    return Owner(name="Jordan", available_start=start, available_end=end, pets=list(pets))

def make_pet(*tasks, species="dog"):
    """Return a Pet with the given tasks."""
    pet = Pet(name="Mochi", species=species, age=3)
    pet.tasks = list(tasks)
    return pet


# ── Existing tests ─────────────────────────────────────────────────────────

def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.tasks) == 0
    pet.tasks.append(Task(title="Feeding", duration_minutes=10, priority="high"))
    assert len(pet.tasks) == 1
    pet.tasks.append(Task(title="Grooming", duration_minutes=20, priority="medium"))
    assert len(pet.tasks) == 2


# ── 1. Priority ordering ───────────────────────────────────────────────────

def test_high_priority_scheduled_before_low():
    low  = Task(title="Grooming",      duration_minutes=10, priority="low")
    high = Task(title="Morning walk",  duration_minutes=10, priority="high")
    pet  = make_pet(low, high)
    scheduler = Scheduler(owner=make_owner(pet))
    scheduler.build_schedule()
    titles = [s.task.title for s in scheduler.scheduled]
    assert titles.index("Morning walk") < titles.index("Grooming")


# ── 2. Time window enforcement ─────────────────────────────────────────────

def test_task_exceeding_window_is_skipped():
    fits      = Task(title="Feeding",      duration_minutes=10,  priority="high")
    too_long  = Task(title="Long session", duration_minutes=200, priority="high")
    pet = make_pet(fits, too_long)
    scheduler = Scheduler(owner=make_owner(pet, start=480, end=570))
    scheduler.build_schedule()
    titles = [s.task.title for s in scheduler.scheduled]
    assert "Long session" not in titles
    assert "Feeding" in titles


# ── 3. Conflict detection ──────────────────────────────────────────────────

def test_conflicting_tasks_flagged_not_double_scheduled():
    t1 = Task(title="Walk",    duration_minutes=30, priority="high", forced_start=480)
    t2 = Task(title="Feeding", duration_minutes=10, priority="high", forced_start=480)
    pet = make_pet(t1, t2)
    scheduler = Scheduler(owner=make_owner(pet))
    scheduler.build_schedule()
    scheduled_titles = [s.task.title for s in scheduler.scheduled]
    # Exactly one of the two makes it in; the other is flagged
    assert len(scheduler.conflicts) == 1
    assert not ("Walk" in scheduled_titles and "Feeding" in scheduled_titles)


# ── 4. Recurring task next-occurrence ─────────────────────────────────────

def test_daily_task_returns_new_instance_on_complete():
    task = Task(title="Morning walk", duration_minutes=30, priority="high", frequency="daily")
    next_task = task.mark_complete()
    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.title == task.title


def test_once_task_returns_none_on_complete():
    task = Task(title="Vet visit", duration_minutes=60, priority="high", frequency="once")
    result = task.mark_complete()
    assert result is None


# ── 5. Species filtering ───────────────────────────────────────────────────

def test_dog_task_excluded_from_cat_schedule():
    dog_task = Task(title="Dog walk", duration_minutes=20, priority="high", required_species="dog")
    cat = make_pet(dog_task, species="cat")
    scheduler = Scheduler(owner=make_owner(cat))
    scheduler.build_schedule()
    assert len(scheduler.scheduled) == 0


# ── 6. Sorting correctness (chronological order) ──────────────────────────

def test_schedule_sorted_chronologically():
    t1 = Task(title="Early task", duration_minutes=10, priority="low",  forced_start=480)
    t2 = Task(title="Late task",  duration_minutes=10, priority="high", forced_start=510)
    pet = make_pet(t2, t1)  # added in reverse order
    scheduler = Scheduler(owner=make_owner(pet))
    scheduler.build_schedule()
    start_times = [s.start_time for s in scheduler.scheduled]
    assert start_times == sorted(start_times)
