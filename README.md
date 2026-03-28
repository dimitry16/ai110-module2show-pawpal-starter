# PawPal+ (Module 2 Project)

<a href="/course_images/ai110/PawPalPlus.png" target="_blank"><img src='/course_images/ai110/PawPalPlus.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Features

- **Priority-based scheduling** — Tasks are sorted high → medium → low before placement; high-priority tasks always appear first in the daily plan.
- **Time window enforcement** — The scheduler only places tasks that fit within the owner's available window; tasks that overflow are skipped and reported.
- **Chronological sorting** — The final schedule is sorted by start time so tasks are displayed in the order they occur, regardless of priority insertion order.
- **Conflict detection** — Tasks pinned to the same time slot via `forced_start` are detected using overlap checking. Conflicting tasks emit a warning and are skipped — the program never crashes.
- **Species filtering** — Tasks with a `required_species` are automatically excluded from pets of a different species at scheduler initialization.
- **Daily and weekly recurrence** — Tasks with `frequency="daily"` or `frequency="weekly"` automatically return a fresh, incomplete copy when marked complete, ready for the next occurrence.
- **Recurrence day filtering** — Tasks with `recur_days` (e.g. `["Mon", "Wed"]`) are only included when `today` matches one of those days.
- **Filter by pet** — `get_tasks_for_pet()` returns only the scheduled tasks belonging to a specific pet.
- **Filter by completion status** — `get_incomplete_tasks()` returns all tasks not yet marked complete; completed tasks are excluded from scheduling automatically.
- **Plan explanation** — `explain_plan()` produces a human-readable summary of scheduled tasks, conflict warnings, skipped tasks, and total time used vs. available.

## Running the app

```bash
python -m streamlit run app.py
```

## Running tests

```bash
python -m pytest tests/ -v
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
