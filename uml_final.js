classDiagram
    class Task {
        +String title
        +int duration_minutes
        +Literal priority
        +String required_species
        +bool completed
        +List~str~ recur_days
        +Literal frequency
        +int forced_start
        +mark_complete() Task
        +is_due_today(today) bool
    }

    class ScheduledTask {
        +Task task
        +int start_time
        +end_time() int
        +start_time_str() str
        +conflicts_with(other) bool
    }

    class Pet {
        +String name
        +String species
        +int age
        +List~Task~ tasks
    }

    class Owner {
        +String name
        +int available_start
        +int available_end
        +List~str~ preferences
        +List~Pet~ pets
        +available_minutes() int
    }

    class Scheduler {
        +Owner owner
        +String today
        +List~Task~ tasks
        +List~ScheduledTask~ scheduled
        +List conflicts
        +build_schedule() List~ScheduledTask~
        +get_tasks_for_pet(pet_name) List~ScheduledTask~
        +get_incomplete_tasks() List~Task~
        +explain_plan() str
    }

    Owner "1" --> "*" Pet : owns
    Pet "1" --> "*" Task : has
    Scheduler --> Owner : schedules for
    Scheduler --> ScheduledTask : produces
    ScheduledTask --> Task : wraps
