from datetime import datetime

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

# Initialize session state for Owner and Pet
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None

owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Create/update Owner and Pet in session state
if st.session_state.owner is None or st.session_state.owner.name != owner_name:
    st.session_state.owner = Owner(name=owner_name)

if st.session_state.pet is None or st.session_state.pet.name != pet_name:
    st.session_state.pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(st.session_state.pet)
else:
    st.session_state.pet.species = species

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

priority_map = {"low": 3, "medium": 2, "high": 1}

if st.button("Add task"):
    task = Task(
        name=task_title,
        duration=int(duration),
        priority=priority_map[priority],
        time=datetime.now(),
    )
    st.session_state.pet.add_task(task)
    st.success(f"✓ Task '{task_title}' added to {st.session_state.pet.name}!")

if st.session_state.pet and st.session_state.pet.get_tasks():
    st.write(f"Tasks for {st.session_state.pet.name}:")
    task_data = [
        {
            "Title": task.name,
            "Duration (min)": task.duration,
            "Priority": task.priority,
            "Status": task.status,
        }
        for task in st.session_state.pet.get_tasks()
    ]
    st.table(task_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule for your pet(s).")

if st.button("Generate schedule"):
    if st.session_state.owner and st.session_state.pet.get_tasks():
        scheduler = Scheduler()
        schedule = scheduler.generate_schedule(st.session_state.owner)

        st.success(f"✓ Schedule generated for {st.session_state.owner.name}!")
        st.markdown("### Today's Schedule")

        if schedule:
            for task in schedule:
                st.markdown(
                    f"**{task.time.strftime('%H:%M')}** — {task.name} ({task.duration} min, priority {task.priority}) — *{task.status}*"
                )
        else:
            st.info("No tasks in schedule.")

        # Check for conflicts
        conflicts = scheduler.detect_conflicts(schedule)
        if conflicts:
            st.warning(f"⚠️ {len(conflicts)} conflict(s) detected:")
            for task1, task2 in conflicts:
                st.markdown(f"- '{task1.name}' overlaps with '{task2.name}'")
    else:
        st.warning("Add at least one task before generating a schedule.")
