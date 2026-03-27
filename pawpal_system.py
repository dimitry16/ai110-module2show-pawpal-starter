from dataclasses import dataclass, field
from typing import List, Literal, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Literal["low", "medium", "high"]
    required_species: Optional[str] = None  # e.g. "dog", "cat", or None for any
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class ScheduledTask:
    task: Task
    start_time: int  # minutes from midnight (e.g. 480 = 8:00am)

    def start_time_str(self) -> str:
        """Return start_time as a human-readable string (e.g. '8:00am')."""
        h, m = divmod(self.start_time, 60)
        period = "am" if h < 12 else "pm"
        h = h if h <= 12 else h - 12
        return f"{h}:{m:02d}{period}"


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
    def __init__(self, owner: Owner):
        """Initialize the scheduler and collect eligible tasks from all of the owner's pets."""
        self.owner = owner
        self.tasks = [
            task
            for pet in owner.pets
            for task in pet.tasks
            if task.required_species is None or task.required_species == pet.species
        ]
        self.scheduled: List[ScheduledTask] = []

    def build_schedule(self) -> List[ScheduledTask]:
        """Order tasks by priority, fit within the owner's time window."""
        sorted_tasks = sorted(self.tasks, key=lambda t: PRIORITY_ORDER[t.priority])
        current_time = self.owner.available_start
        self.scheduled = []

        for task in sorted_tasks:
            if current_time + task.duration_minutes <= self.owner.available_end:
                self.scheduled.append(ScheduledTask(task=task, start_time=current_time))
                current_time += task.duration_minutes

        return self.scheduled

    def explain_plan(self) -> str:
        """Return a human-readable explanation of scheduled and skipped tasks."""
        if not self.scheduled:
            return "No tasks were scheduled."

        scheduled_tasks = [st.task for st in self.scheduled]
        lines = ["Today's Schedule", "=" * 30]

        for st in self.scheduled:
            lines.append(
                f"  {st.start_time_str()}  [{st.task.priority.upper()}]  "
                f"{st.task.title} ({st.task.duration_minutes} min)"
            )

        skipped = [t for t in self.tasks if id(t) not in {id(st) for st in scheduled_tasks}]
        if skipped:
            lines.append("\nSkipped (not enough time):")
            for t in skipped:
                lines.append(f"  - {t.title} ({t.duration_minutes} min, {t.priority})")

        total = sum(st.task.duration_minutes for st in self.scheduled)
        lines.append(f"\nTotal scheduled: {total} / {self.owner.available_minutes} min available")
        return "\n".join(lines)
