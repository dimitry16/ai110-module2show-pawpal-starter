# PawPal+ Project Reflection

## 1. System Design
- This application is designed to help pet owners organize their daily responsibilities in a simple way. Users shohuld be able to enter basic information about themselves and their pets. The app allows users to add and edit tasks, with each task including key details such as duration and priority level. Using this information, the app should generate daily schedule that balances constraints and prioritizes the most important activities. The resulting plan is displayed in a simple and user-friendly format, with an explanation of how scheduling decisions were made to improve. Includes tests for scheduling behaviors, such as adding a pet, scheduling a walk, and verifying that daily tasks are correctly generated and organized.

**a. Initial design**

- Briefly describe your initial UML design.
UML design models a pet care management system that generates a daily care plan based on task priorities. The system has a object-oriented structure, where each class has a focused responsibility, and the Scheduler acts as the main entity for making decisons.

- What classes did you include, and what responsibilities did you assign to each?
Task
    Responsibility: Represents a single care action for a pet
Pet
    Responsibility: Stores pet info that may influence which tasks are needed
Owner
    Responsibility: Represents the person's constraints and preferences for scheduling
Scheduler
    Responsibility: Builds and explains a daily care plan by ordering tasks based on priority and time constraints

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.

priority now uses Literal — invalid values are caught by type checkers
Added ScheduledTask dataclass pairing a Task with a start_time
Replaced available_minutes with available_start/available_end for a real time window, with available_minutes as a computed property
Added required_species to Task so species-specific tasks can be filtered
self.scheduled stores the result of build_schedule so explain_plan can reference it

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The scheduler uses a greedy, priority-first placement strategy: it sorts all tasks by priority and places each one sequentially, skipping any that don't fit in the remaining time window. This means a large low-priority task placed early can block several smaller high-priority tasks that would otherwise fit.

For example, if a 60-minute "Grooming" task is scheduled before a 5-minute "Administer medication" task because both share the same priority level, the medication may get skipped even though it would have easily fit.

This tradeoff is reasonable for a pet care planning assistant because the logic stays simple and predictable — owners can understand and override it manually. A more optimal approach such as bin-packing or backtracking search would find better schedules but would be significantly harder to explain to a non-technical user.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
