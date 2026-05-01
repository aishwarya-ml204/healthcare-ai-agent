import streamlit as st
import json
import pandas as pd

file_name = "health_data.json"

# ---------- Health Advice ----------
def health_advice(systolic, diastolic, bmi):
    if systolic > 140 or diastolic > 90:
        return "⚠ High BP! Reduce salt & consult doctor."
    elif systolic < 90 or diastolic < 60:
        return "⚠ Low BP! Improve nutrition."
    elif bmi > 25:
        return "⚠ Overweight! Exercise regularly."
    elif bmi < 18.5:
        return "⚠ Underweight! Eat healthy food."
    else:
        return "✅ You are healthy!"

# ---------- Health Risk ----------
def health_risk(s, d, bmi):
    if s > 140 or d > 90:
        return "🔴 High Risk"
    elif bmi > 30:
        return "🟠 Moderate Risk"
    else:
        return "🟢 Low Risk"

# ---------- Chatbot ----------
def ai_chatbot(query):
    q = query.lower()

    if "low bp" in q:
        return """For Low BP:
- Increase salt intake slightly
- Drink more water
- Eat small frequent meals"""

    elif "high bp" in q:
        return """For High BP:
- Reduce salt intake
- Exercise regularly
- Eat healthy food"""

    elif "diet" in q:
        return """Healthy Diet:
- Fruits & vegetables
- Whole grains
- Avoid junk food"""

    elif "exercise" in q:
        return "Do at least 30 minutes of exercise daily."

    elif "diabetes" in q:
        return "Avoid sugar, eat balanced meals, and exercise regularly."

    else:
        return "Consult a doctor for proper medical advice."

# ---------- Load/Save ----------
def load_data():
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

# ---------- UI ----------
st.set_page_config(page_title="Healthcare AI", layout="centered")
st.title("🏥 Healthcare Monitoring AI Agent")
st.markdown("### 💙 Your Smart Health Assistant")

menu = [
    "🏠 Home",
    "➕ Add Patient",
    "📄 View Patient",
    "💬 Chatbot",
    "💊 Reminder",
    "🎯 Goals",
    "💡 Health Tips",
    "👨‍👩‍👧 Caregiver"
]

choice = st.sidebar.selectbox("Menu", menu)

# ---------- HOME ----------
if choice == "🏠 Home":
    st.write("Welcome to Healthcare Monitoring System")
    st.info("Track BP, BMI, get advice, chatbot, reminders, and goals")

# ---------- ADD PATIENT ----------
elif choice == "➕ Add Patient":
    st.subheader("Add Patient Data")

    pid = st.text_input("Patient ID")
    systolic = st.number_input("Systolic BP")
    diastolic = st.number_input("Diastolic BP")
    bmi = st.number_input("BMI")

    if st.button("Submit"):
        advice = health_advice(systolic, diastolic, bmi)
        data = load_data()

        data[pid] = {
            "Systolic": systolic,
            "Diastolic": diastolic,
            "BMI": bmi,
            "Advice": advice
        }

        save_data(data)

        st.success("Data Saved!")
        st.write("Advice:", advice)
        st.write("Risk Level:", health_risk(systolic, diastolic, bmi))

# ---------- VIEW PATIENT ----------
elif choice == "📄 View Patient":
    st.subheader("Patient Details")

    pid = st.text_input("Enter Patient ID")

    if "patient" not in st.session_state:
        st.session_state.patient = None

    data = load_data()

    if st.button("Search"):
        if pid in data:
            st.session_state.patient = data[pid]
        else:
            st.error("Patient not found")

    if st.session_state.patient:
        patient = st.session_state.patient

        st.json(patient)

        # Graph
        st.subheader("Health Graph")
        st.bar_chart({
            "Systolic": [patient["Systolic"]],
            "Diastolic": [patient["Diastolic"]],
            "BMI": [patient["BMI"]]
        })

        # Health Insights
        st.subheader("Health Insights")

        if patient["BMI"] > 25:
            st.warning("Overweight - Exercise recommended")
        elif patient["BMI"] < 18.5:
            st.warning("Underweight - Improve diet")
        else:
            st.success("Healthy BMI")

        # Report
        if st.button("Generate Report"):
            st.subheader("Patient Report")
            st.write("BP:", f"{patient['Systolic']}/{patient['Diastolic']}")
            st.write("BMI:", patient["BMI"])
            st.write("Advice:", patient["Advice"])

        # CSV Download
        df = pd.DataFrame(data).T
        csv = df.to_csv(index=True).encode('utf-8')

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="health_data.csv",
            mime="text/csv"
        )

# ---------- CHATBOT ----------
elif choice == "💬 Chatbot":
    st.subheader("AI Health Chatbot")

    if "history" not in st.session_state:
        st.session_state.history = []

    query = st.text_input("Ask a question")

    if st.button("Ask AI"):
        response = ai_chatbot(query)

        st.session_state.history.append(("You", query))
        st.session_state.history.append(("Bot", response))

    for role, msg in st.session_state.history:
        st.write(f"**{role}:** {msg}")

    if st.button("Clear Chat"):
        st.session_state.history = []

# ---------- REMINDER ----------
elif choice == "💊 Reminder":
    st.subheader("Medication Reminder")

    med = st.text_input("Medicine Name")
    time = st.time_input("Select Time")
    taken = st.checkbox("Mark as Taken")

    if st.button("Save Reminder"):
        st.success(f"Reminder set for {med} at {time}")
        st.write("Status:", "✅ Taken" if taken else "❌ Not Taken")

    # Adherence Tracking
    st.subheader("Medication Adherence")

    adherence = st.slider("Doses taken this week", 0, 7)

    if adherence >= 5:
        st.success("Good adherence 👍")
    else:
        st.warning("Improve consistency ⚠")

# ---------- GOALS ----------
elif choice == "🎯 Goals":
    st.subheader("Health Goals")

    goal = st.text_input("Enter your goal")
    progress = st.slider("Progress (%)", 0, 100)

    if st.button("Save Goal"):
        st.success("Goal saved successfully!")

    st.progress(progress / 100)

    if progress < 50:
        st.warning("Keep going 💪")
    else:
        st.success("Great progress 🎉")

# ---------- HEALTH TIPS ----------
elif choice == "💡 Health Tips":
    st.subheader("Daily Health Tips")

    st.write("✔ Drink 2–3 liters of water")
    st.write("✔ Exercise daily")
    st.write("✔ Eat balanced diet")
    st.write("✔ Sleep 7–8 hours")

# ---------- CAREGIVER ----------
elif choice == "👨‍👩‍👧 Caregiver":
    st.subheader("Caregiver Monitoring")

    pid = st.text_input("Enter Patient ID")
    data = load_data()

    if st.button("Check Patient"):
        if pid in data:
            st.json(data[pid])
        else:
            st.error("Patient not found")
