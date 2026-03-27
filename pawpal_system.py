from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", or "high"


@dataclass
class Pet:
    name: str
    species: str
    age: int


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: List[str] = field(default_factory=list)


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task]):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    def build_schedule(self) -> List[Task]:
        """Return an ordered list of tasks that fit within the owner's available time."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why each task was chosen and when."""
        pass
