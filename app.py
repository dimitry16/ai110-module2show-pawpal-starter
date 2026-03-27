import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant.")

# --- Initialize session state ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = []          # List[Pet]
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

st.divider()

# ── Section 1: Owner Setup ──────────────────────────────────────────────────
st.subheader("1. Owner Setup")

owner_name = st.text_input("Your name", value="Jordan")
col1, col2 = st.columns(2)
with col1:
    available_start = st.number_input(
        "Available from (minutes from midnight)",
        min_value=0, max_value=1439, value=480, step=30,
        help="480 = 8:00am"
    )
with col2:
    available_end = st.number_input(
        "Available until (minutes from midnight)",
        min_value=0, max_value=1439, value=570, step=30,
        help="570 = 9:30am"
    )

if st.button("Save Owner"):
    st.session_state.owner = Owner(
        name=owner_name,
        available_start=int(available_start),
        available_end=int(available_end),
        pets=st.session_state.pets,
    )
    st.session_state.scheduler = None
    st.success(f"Owner '{owner_name}' saved with a {st.session_state.owner.available_minutes}-minute window.")

st.divider()

# ── Section 2: Add a Pet ────────────────────────────────────────────────────
st.subheader("2. Add a Pet")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.warning("Save an owner first.")
    else:
        new_pet = Pet(name=pet_name, species=species, age=age)
        st.session_state.pets.append(new_pet)
        st.session_state.owner.pets = st.session_state.pets
        st.session_state.scheduler = None
        st.success(f"Added {species} '{pet_name}' (age {age}).")

if st.session_state.pets:
    st.write("Your pets:")
    st.table([{"name": p.name, "species": p.species, "age": p.age} for p in st.session_state.pets])

st.divider()

# ── Section 3: Add a Task ───────────────────────────────────────────────────
st.subheader("3. Schedule a Task")

if not st.session_state.pets:
    st.info("Add at least one pet before scheduling tasks.")
else:
    pet_names = [p.name for p in st.session_state.pets]
    selected_pet_name = st.selectbox("Assign task to", pet_names)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add Task"):
        target_pet = next(p for p in st.session_state.pets if p.name == selected_pet_name)
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            required_species=target_pet.species,
            frequency=frequency,
        )
        target_pet.tasks.append(task)
        st.session_state.scheduler = None
        st.success(f"Task '{task_title}' added to {selected_pet_name} ({frequency}).")

    all_tasks = [(p.name, t) for p in st.session_state.pets for t in p.tasks]
    if all_tasks:
        st.write("All tasks:")

        # ── Filters ──────────────────────────────────────────────────────────
        fcol1, fcol2 = st.columns(2)
        with fcol1:
            filter_pet = st.selectbox("Filter by pet", ["All"] + pet_names, key="filter_pet")
        with fcol2:
            filter_status = st.selectbox("Filter by status", ["All", "Incomplete", "Completed"], key="filter_status")

        filtered = [
            (pet, t) for pet, t in all_tasks
            if (filter_pet == "All" or pet == filter_pet)
            and (
                filter_status == "All"
                or (filter_status == "Completed" and t.completed)
                or (filter_status == "Incomplete" and not t.completed)
            )
        ]

        if filtered:
            for pet_name_f, t in filtered:
                tcol1, tcol2, tcol3, tcol4, tcol5 = st.columns([3, 2, 2, 2, 2])
                tcol1.write(f"**{t.title}**")
                tcol2.write(t.priority)
                tcol3.write(f"{t.duration_minutes} min")
                tcol4.write(f"_{t.frequency}_")
                if t.completed:
                    tcol5.write("✓ done")
                else:
                    if tcol5.button("Mark done", key=f"done_{id(t)}"):
                        target_pet = next(p for p in st.session_state.pets if pet_name_f in [p.name])
                        next_task = t.mark_complete()
                        if next_task:
                            target_pet.tasks.append(next_task)
                            st.success(f"'{t.title}' completed — next occurrence queued.")
                        else:
                            st.success(f"'{t.title}' marked complete.")
                        st.session_state.scheduler = None
                        st.rerun()
        else:
            st.info("No tasks match the selected filters.")

st.divider()

# ── Section 4: Generate Schedule ────────────────────────────────────────────
st.subheader("4. Generate Schedule")

if st.button("Build Schedule"):
    if st.session_state.owner is None:
        st.warning("Save an owner first.")
    elif not any(p.tasks for p in st.session_state.pets):
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner=st.session_state.owner)
        scheduler.build_schedule()
        st.session_state.scheduler = scheduler

if st.session_state.scheduler is not None:
    sched = st.session_state.scheduler
    if sched.scheduled:
        st.success(f"Scheduled {len(sched.scheduled)} task(s).")
        st.table([
            {
                "time": item.start_time_str(),
                "task": item.task.title,
                "pet": next(
                    (p.name for p in st.session_state.pets if item.task in p.tasks), "—"
                ),
                "duration (min)": item.task.duration_minutes,
                "priority": item.task.priority,
            }
            for item in sched.scheduled
        ])
        skipped = [t for t in sched.tasks if id(t) not in {id(item.task) for item in sched.scheduled}]
        if skipped:
            st.warning(f"{len(skipped)} task(s) skipped (not enough time):")
            for t in skipped:
                st.write(f"- {t.title} ({t.duration_minutes} min, {t.priority})")
    else:
        st.error("No tasks fit within the owner's available time window.")
