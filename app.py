import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# ---------------- LOAD ENV ----------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="FocusFlow AI", layout="centered")
st.title("📅 FocusFlow AI – AI Task Planner Agent")


# ---------------- INPUT ----------------
tasks_input = st.text_area("Enter your tasks")


# ---------------- AI PRIORITY CLASSIFIER ----------------
def classify_task(task):
    prompt = f"""
You are an AI task prioritization assistant.

Classify the task into exactly one category:
High, Medium, Low

Rules:
High = urgent, deadline, exam, project, submission
Medium = study, practice, learning, revision
Low = general or optional tasks

Task: {task}

Return ONLY one word: High, Medium, or Low
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a strict classifier."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


# ---------------- PRIORITY GROUPING ----------------
def prioritize_tasks(tasks):
    high, medium, low = [], [], []

    for task in tasks:
        if not task.strip():
            continue

        category = classify_task(task).lower()

        if "high" in category:
            high.append(task)
        elif "medium" in category:
            medium.append(task)
        else:
            low.append(task)

    return high, medium, low


# ---------------- AI SCHEDULER ----------------
def generate_plan(high, medium, low):

    prompt = f"""
You are a productivity AI agent.

Create a structured daily schedule with time blocks.

High Priority Tasks:
{high}

Medium Priority Tasks:
{medium}

Low Priority Tasks:
{low}

Make it simple, practical, and time-based for a student.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful productivity assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ---------------- MAIN UI FLOW ----------------
if st.button("Generate Plan"):

    if not tasks_input.strip():
        st.warning("Please enter tasks")
    else:

        tasks = tasks_input.split("\n")

        # Step 1: AI PRIORITY
        high, medium, low = prioritize_tasks(tasks)

        st.subheader("📌 Task Priority Order")

        st.write("🔴 High Priority:", ", ".join(high) if high else "None")
        st.write("🟡 Medium Priority:", ", ".join(medium) if medium else "None")
        st.write("🟢 Low Priority:", ", ".join(low) if low else "None")

        st.markdown("---")

        # Step 2: AI PLAN
        st.subheader("🤖 AI Generated Daily Plan")

        plan = generate_plan(high, medium, low)
        st.write(plan)