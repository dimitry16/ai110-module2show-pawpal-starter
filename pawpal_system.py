from dataclasses import dataclass, field, replace
from typing import List, Literal, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Literal["low", "medium", "high"]
    required_species: Optional[str] = None  # e.g. "dog", "cat", or None for any
    completed: bool = False
    recur_days: List[str] = field(default_factory=list)  # e.g. ["Mon", "Wed", "Fri"]
    frequency: Literal["once", "daily", "weekly"] = "once"
    forced_start: Optional[int] = None  # pin task to a specific start time (minutes from midnight)

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and return a fresh instance if it recurs, else None."""
        self.completed = True
        if self.frequency in ("daily", "weekly"):
            return replace(self, completed=False)
        return None

    def is_due_today(self, today: str) -> bool:
        """Return True if the task recurs on today (e.g. 'Mon'), or has no recurrence set."""
        if not self.recur_days:
            return True
        return today in self.recur_days


@dataclass
class ScheduledTask:
    task: Task
    start_time: int  # minutes from midnight (e.g. 480 = 8:00am)

    @property
    def end_time(self) -> int:
        """Return the minute at which this task ends."""
        return self.start_time + self.task.duration_minutes

    def start_time_str(self) -> str:
        """Return start_time as a human-readable string (e.g. '8:00am')."""
        h, m = divmod(self.start_time, 60)
        period = "am" if h < 12 else "pm"
        h = h if h <= 12 else h - 12
        return f"{h}:{m:02d}{period}"

    def conflicts_with(self, other: "ScheduledTask") -> bool:
        """Return True if this task's time slot overlaps with another scheduled task."""
        return self.start_time < other.end_time and other.start_time < self.end_time


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)


@dataclass
class Owner:
    name: str
    available_start: int   # minutes from midnight (e.g. 480 = 8:00am)
    available_end: int     # minutes from midnight (e.g. 1200 = 8:00pm)
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    @property
    def available_minutes(self) -> int:
        """Return the total number of minutes the owner is available today."""
        return self.available_end - self.available_start


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Scheduler:
    def __init__(self, owner: Owner, today: str = ""):
        """Initialize the scheduler and collect eligible tasks from all of the owner's pets."""
        self.owner = owner
        self.today = today  # e.g. "Mon", "Tue" — used for recurring task filtering
        self.tasks = [
            task
            for pet in owner.pets
            for task in pet.tasks
            if (task.required_species is None or task.required_species == pet.species)
            and not task.completed
            and task.is_due_today(today)
        ]
        self.scheduled: List[ScheduledTask] = []
        self.conflicts: List[tuple] = []  # pairs of conflicting ScheduledTasks

    def build_schedule(self) -> List[ScheduledTask]:
        """Sort tasks by priority, fit within the owner's time window, detect conflicts."""
        sorted_tasks = sorted(self.tasks, key=lambda t: PRIORITY_ORDER[t.priority])
        current_time = self.owner.available_start
        self.scheduled = []
        self.conflicts = []

        for task in sorted_tasks:
            start = task.forced_start if task.forced_start is not None else current_time
            if start + task.duration_minutes > self.owner.available_end:
                continue  # doesn't fit in window
            candidate = ScheduledTask(task=task, start_time=start)
            # Conflict detection: warn but don't crash
            overlaps = [s for s in self.scheduled if candidate.conflicts_with(s)]
            if overlaps:
                clash = overlaps[0]
                warning = (
                    f"WARNING: '{task.title}' ({candidate.start_time_str()}, {task.duration_minutes} min) "
                    f"conflicts with '{clash.task.title}' ({clash.start_time_str()}, {clash.task.duration_minutes} min) "
                    f"- skipping '{task.title}'."
                )
                self.conflicts.append((candidate, clash, warning))
            else:
                self.scheduled.append(candidate)
                current_time = max(current_time, start + task.duration_minutes)

        # Sort final schedule by start time for display
        self.scheduled.sort(key=lambda s: s.start_time)
        return self.scheduled

    def get_tasks_for_pet(self, pet_name: str) -> List[ScheduledTask]:
        """Return only the scheduled tasks assigned to the given pet."""
        pet_tasks = {
            id(task)
            for pet in self.owner.pets
            if pet.name == pet_name
            for task in pet.tasks
        }
        return [s for s in self.scheduled if id(s.task) in pet_tasks]

    def get_incomplete_tasks(self) -> List[Task]:
        """Return all eligible tasks that have not been marked complete."""
        return [t for t in self.tasks if not t.completed]

    def explain_plan(self) -> str:
        """Return a human-readable explanation of scheduled and skipped tasks."""
        if not self.scheduled:
            return "No tasks were scheduled."

        scheduled_ids = {id(s.task) for s in self.scheduled}
        lines = ["Today's Schedule", "=" * 30]

        for s in self.scheduled:
            lines.append(
                f"  {s.start_time_str()}  [{s.task.priority.upper()}]  "
                f"{s.task.title} ({s.task.duration_minutes} min)"
            )

        if self.conflicts:
            lines.append("\nConflicts detected (skipped):")
            for *_, warning in self.conflicts:
                lines.append(f"  {warning}")

        skipped = [t for t in self.tasks if id(t) not in scheduled_ids]
        if skipped:
            lines.append("\nSkipped (not enough time):")
            for t in skipped:
                lines.append(f"  - {t.title} ({t.duration_minutes} min, {t.priority})")

        total = sum(s.task.duration_minutes for s in self.scheduled)
        lines.append(f"\nTotal scheduled: {total} / {self.owner.available_minutes} min available")
        return "\n".join(lines)
