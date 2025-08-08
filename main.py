import os
import time
import threading
import itertools
import streamlit as st
from graph import Get_workflow as build_graph

st.set_page_config(page_title="Diet Plan Input", layout="centered")
st.title("🥗 Diet Plan Generator - Patient Input Form")

# Initialize dynamic list session states
for key in ["likes", "dislikes", "supper_snacks", "breakfast", "lunch", "dinner"]:
    if key not in st.session_state:
        st.session_state[key] = []

# Display tags with delete buttons
def display_tags(title, key, emoji="🍽️"):
    items = st.session_state[key]
    if items:
        st.markdown(f"**{emoji} {title}:**")
        cols = st.columns(len(items))
        for i, (item, col) in enumerate(zip(items, cols)):
            with col:
                st.markdown(
                    f"""
                    <div style='
                        background-color:#e0f7fa;
                        padding:6px 10px;
                        border-radius:25px;
                        margin:5px 0;
                        border:1px solid #4dd0e1;
                        color:#006064;
                        font-size:0.9em;
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                    '><span>{item}</span></div>
                    """, unsafe_allow_html=True)
                if st.button("✖", key=f"delete_{key}_{i}"):
                    st.session_state[key].pop(i)
                    st.rerun()
    else:
        st.markdown(f"🕳️ No {title.lower()} added yet.")

# Add items to list
def add_item(item, key):
    if item and item.strip():
        st.session_state[key].append(item.strip())

# --- Core Input Form ---
with st.form("diet_form"):
    name = st.text_input("👤 Name", "Hassan")
    age = st.number_input("🎂 Age", min_value=1, max_value=90, value=29)
    gender = st.selectbox("⚧️ Gender", ["MALE", "FEMALE", "BISEXUAL", "OTHER"])
    height_m = st.number_input("📏 Height (meters)", 0.6, 2.0, value=1.75)
    weight_kg = st.number_input("⚖️ Weight (kg)", 30, 200, value=85)
    primary_goal = st.selectbox("🎯 Goal", ["LOSE_WEIGHT", "GAIN_WEIGHT", "MAINTAIN_WEIGHT"])
    diet_type = st.selectbox("🍽️ Diet Type", ["VEGETARIAN", "NON_VEGETARIAN", "VEGAN"])
    allergies = st.text_input("🚫 Allergies (comma separated)", "Lactose").split(",")
    medical_conditions = st.text_input("🩺 Medical Conditions (comma separated)", "Diabetes").split(",")
    activity_level_description = st.text_area("🏃‍♂️ Activity Description", 
        "I walk 30-40 mins daily and go to the gym 3x/week for light training.")
    wake_time = st.time_input("⏰ Wake Time")
    sleep_time = st.time_input("😴 Sleep Time")
    meal_frequency = st.slider("🍽️ Meals per Day", 2, 10, 3)
    water_intake_liters = st.slider("💧 Water Intake (Liters)", 0.5, 6.0, 2.5, step=0.1)
    submitted = st.form_submit_button("✅ Save Core Info")

# --- Dynamic Inputs ---
st.markdown("---")

for label, key, emoji in [
    ("Liked Food", "likes", "✅"),
    ("Disliked Food", "dislikes", "❌"),
    ("Supper Snack", "supper_snacks", "🍿"),
    ("Breakfast Item", "breakfast", "☀️"),
    ("Lunch Item", "lunch", "🍱"),
    ("Dinner Item", "dinner", "🌙"),
]:
    col = st.columns(2)[0 if "Supper" in label or "Liked" in label or "Lunch" in label else 1]
    with col:
        item = st.text_input(f"{emoji} Add {label}", key=f"new_{key}")
        if st.button(f"Add to {label}", key=f"btn_{key}"):
            add_item(item, key)
    display_tags(label, key, emoji)

# Sidebar Inputs
api_key = st.sidebar.text_input("🔑 Google API Key", type="password", placeholder="Enter your Google API key...")

# Generate Plan
if st.button("Generate Diet plan"):
    if not api_key.strip():
        st.warning("⚠️ Please enter your Google API key.")
    else:
        os.environ["GOOGLE_API_KEY"] = api_key

        # Prepare full state from inputs and session state
        state = {
            "name": name,
            "age": int(age),
            "gender": gender.capitalize(),
            "height_m": height_m,
            "weight_kg": weight_kg,
            "primary_goal": primary_goal.replace("_", " ").capitalize(),
            "diet_type": diet_type.replace("_", "-").capitalize(),
            "allergies": [a.strip() for a in allergies if a.strip()],
            "medical_conditions": [m.strip() for m in medical_conditions if m.strip()],
            "activity_level_description": activity_level_description.strip(),
            "wake_time": wake_time.strftime("%H:%M"),
            "sleep_time": sleep_time.strftime("%H:%M"),
            "meal_frequency": int(meal_frequency),
            "water_intake_liters": float(water_intake_liters),
            "likes": st.session_state.likes,
            "dislikes": st.session_state.dislikes,
            "supper_snacks": st.session_state.supper_snacks,
            "breakfast": st.session_state.breakfast,
            "lunch": st.session_state.lunch,
            "dinner": st.session_state.dinner
        }

        # Progress Messages
        progress_messages = [
            "🔍 Analyzing your client request...",
            "🧠 Identifying health needs...",
            "📐 Designing personalized meals...",
            "🛒 Compiling ingredient list...",
            "📝 Finalizing the diet PDF...",
        ]

        status_placeholder = st.empty()
        final_state = {}

        def run_graph():
            graph = build_graph()
            result = graph.invoke(state)
            final_state.update(result)

        thread = threading.Thread(target=run_graph)
        thread.start()

        for msg in itertools.cycle(progress_messages):
            if not thread.is_alive():
                break
            status_placeholder.info(msg)
            time.sleep(4)

        thread.join()
        status_placeholder.empty()

        # Show result
        if "diet_plan_pdf" in final_state:
            st.success("✅ Diet Plan Generated Successfully!")
            st.download_button(
                label="📄 Download Diet Plan PDF",
                data=final_state["diet_plan_pdf"],
                file_name=f"DIET_PLAN.pdf",
                mime="application/pdf"
            )
        else:
            st.error("❌ Diet plan generation failed.")
