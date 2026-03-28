# PawPal+ Project Reflection

## 1. System Design

This application is designed to help pet owners organize their daily responsibilities in a simple way. Users should be able to enter basic information about themselves and their pets. The app allows users to add and edit tasks, with each task including key details such as duration and priority level. Using this information, the app generates a daily schedule that balances constraints and prioritizes the most important activities. The resulting plan is displayed in a user-friendly format, with an explanation of how scheduling decisions were made. Includes tests for scheduling behaviors, such as adding a pet, scheduling a walk, and verifying that daily tasks are correctly generated and organized.

**a. Initial design**

- Briefly describe your initial UML design.

  The UML design models a pet care management system that generates a daily care plan based on task priorities. The system has an object-oriented structure, where each class has a focused responsibility, and the Scheduler acts as the main entity for making decisions.

- What classes did you include, and what responsibilities did you assign to each?

  - **Task** — Represents a single care action for a pet
  - **Pet** — Stores pet info that may influence which tasks are needed
  - **Owner** — Represents the person's constraints and preferences for scheduling
  - **Scheduler** — Builds and explains a daily care plan by ordering tasks based on priority and time constraints

**b. Design changes**

- Did your design change during implementation? Yes

- If yes, describe at least one change and why you made it.

  - `priority` now uses `Literal` — invalid values are caught by type checkers
  - Added `ScheduledTask` dataclass pairing a `Task` with a `start_time`
  - Replaced `available_minutes` with `available_start`/`available_end` for a real time window, with `available_minutes` as a computed property
  - Added `required_species` to `Task` so species-specific tasks can be filtered
  - `self.scheduled` stores the result of `build_schedule` so `explain_plan` can reference it

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

  - **Priority** — tasks sorted high to medium to low; higher priority always schedules first
  - **Time window** — tasks that exceed `available_start`/`available_end` are skipped
  - **Duration** — accumulated per task; stops when the window is full
  - **Species** — mismatched `required_species` tasks are filtered before scheduling
  - **Completion status** — already-done tasks are excluded automatically
  - **Recurrence day** — tasks only included if today matches `recur_days`
  - **Forced start** — pinned tasks checked for time conflicts before placement

- How did you decide which constraints mattered most?

  Time and priority came first — without them the scheduler has no stopping condition and no way to choose between tasks. Species and completion filtering came next to eliminate invalid inputs early. Recurrence and forced start were added last as optional constraints that don't affect the core scheduling loop.

**b. Tradeoffs**

The current scheduler uses a priority-first placement strategy. It sorts all tasks by priority and places each one sequentially, skipping any that don't fit in the remaining time window. Therefore, a large low-priority task placed early can block several smaller high-priority tasks.

For example, if a 60-minute "Grooming" task is scheduled before a 5-minute "Administer medication" task because both share the same priority level, the medication may get skipped even though it would have easily fit.

This tradeoff is reasonable for a pet care planning assistant because the logic stays simple and predictable — owners can understand and override it manually. A more optimal approach such as bin-packing or backtracking search would find better schedules but would be significantly harder to explain to a non-technical user.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

  When running into bugs, I explicitly described the bug to Claude and most of the time the correct fix and an explanation of what was causing the bug was provided.

- What kinds of prompts or questions were most helpful?

  Asking Claude to not change the code before I reviewed it was helpful in keeping track of what was being changed and how it would affect the rest of the program.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

  When implementing `conflicts_with()` and wiring it into `build_schedule()`, the logic had a structural flaw: because tasks were placed sequentially with `current_time` always advancing, two tasks could never actually land at the same time slot. The conflict code existed but could never fire.

- How did you evaluate or verify what the AI suggested?

  By running the code and reviewing the output to make sure it was doing what it was supposed to do in the context of the current program.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

  1. Priority ordering
  2. Time window enforcement
  3. Conflict detection
  4. Recurring task next-occurrence
  5. Species filtering

- Why were these tests important?

  To make sure that the features the app offers are working correctly and that it is in fact offering real value to the user.

**b. Confidence**

- How confident are you that your scheduler works correctly?

  Confidence: 4/5

- What edge cases would you test next if you had more time?

  1. Zero available time — `available_start == available_end` should return an empty schedule without crashing
  2. All tasks same priority — order should still be deterministic and chronological

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

  The final app looks great and there were no major conflicts while using Claude.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

  The way a prompt is written can change the results from Claude. In the future, I will make sure the prompts are more clear and more detailed.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

  AI is definitely a tool that can improve the speed of building software. However, software engineers are still the architects who design and put the pieces together while the AI writes the code.
