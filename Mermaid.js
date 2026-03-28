classDiagram
    class Task {
        +String title
        +int duration_minutes
        +String priority
    }

    class Pet {
        +String name
        +String species
        +int age
    }

    class Owner {
        +String name
        +int available_minutes
        +List preferences
    }

    class Scheduler {
        +Owner owner
        +Pet pet
        +List~Task~ tasks
        +build_schedule()
        +explain_plan()
    }

    Scheduler --> Owner
    Scheduler --> Pet
    Scheduler --> Task
