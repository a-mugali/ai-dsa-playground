import requests
import streamlit as st

# --------------------------------
# Config
# --------------------------------

BACKEND_URL = "http://127.0.0.1:8000"


st.set_page_config(page_title="AI Practice Planner", layout="wide")

st.title("📘 AI Practice Planner")


# --------------------------------
# Generate Plan Section
# --------------------------------

st.header("🕒 Study Settings")

col1, col2, col3 = st.columns(3)

with col1:
    time_limit = st.number_input(
        "Daily Time (minutes)", min_value=10, max_value=300, value=60, step=5
    )

with col2:
    min_d = st.slider("Min Difficulty", 1, 10, 3)

with col3:
    max_d = st.slider("Max Difficulty", 1, 10, 7)


if st.button("🚀 Generate Plan"):

    payload = {"time": time_limit, "min_d": min_d, "max_d": max_d}

    try:
        res = requests.post(f"{BACKEND_URL}/generate_plan", json=payload, timeout=10)

        res.raise_for_status()

        plan = res.json()

        if not plan:
            st.warning("No suitable problems found.")
        else:
            st.success("Study plan generated!")

            st.session_state["plan"] = plan

    except Exception as e:
        st.error(f"Backend error: {e}")


# --------------------------------
# Display Plan
# --------------------------------

if "plan" in st.session_state:

    st.header("📋 Today's Study Plan")

    plan = st.session_state["plan"]

    for i, p in enumerate(plan, start=1):

        st.markdown(f"""
            **{i}. {p['title']}**

            • Topic: {', '.join(p['topics'])}
            • Time: {p['duration']} min
            • Difficulty: {p['difficulty']}
            """)

        st.divider()


# --------------------------------
# Feedback Section
# --------------------------------

if "plan" in st.session_state:

    st.header("📝 Feedback")

    feedback_list = []

    for p in st.session_state["plan"]:

        choice = st.radio(
            f"Feedback for {p['title']}",
            ["too_easy", "just_right", "too_hard"],
            horizontal=True,
            key=f"fb_{p['id']}",
        )

        feedback_list.append({"problem_id": p["id"], "feedback": choice})

    if st.button("✅ Submit Feedback"):

        payload = {"feedback": feedback_list}

        try:
            res = requests.post(f"{BACKEND_URL}/feedback", json=payload, timeout=10)

            res.raise_for_status()

            st.success("Feedback submitted!")

        except Exception as e:
            st.error(f"Failed to send feedback: {e}")
