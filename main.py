from pawpal_system import Task, Pet, Owner, Scheduler

# --- Tasks ---
morning_walk = Task(title="Morning walk", duration_minutes=30, priority="high", required_species="dog", forced_start=480)
feeding      = Task(title="Feeding",       duration_minutes=10, priority="high", forced_start=480)   # conflicts with morning_walk
grooming     = Task(title="Grooming",      duration_minutes=20, priority="medium")
vet_meds     = Task(title="Administer medication", duration_minutes=5, priority="high")
litter_box   = Task(title="Clean litter box", duration_minutes=15, priority="low", required_species="cat")

# --- Pets ---
mochi = Pet(name="Mochi", species="dog", age=3, tasks=[morning_walk, grooming])
luna  = Pet(name="Luna",  species="cat", age=5, tasks=[feeding, vet_meds, litter_box])

# --- Owner (available 8:00am - 9:30am = 90 min) ---
jordan = Owner(
    name="Jordan",
    available_start=480,   # 8:00am
    available_end=570,     # 9:30am
    pets=[mochi, luna],
)

# --- Schedule ---
scheduler = Scheduler(owner=jordan)
scheduler.build_schedule()
print(scheduler.explain_plan())
