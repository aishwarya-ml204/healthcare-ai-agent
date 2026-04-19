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

# ---------- Load Data ----------
def load_data():
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except:
        return {}

# ---------- Save Data ----------
def save_data(data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

# ---------- UI ----------
st.set_page_config(page_title="Healthcare AI", layout="centered")
st.title("🏥 Healthcare Monitoring AI Agent")

menu = ["🏠 Home", "➕ Add Patient", "📄 View Patient", "💬 Chatbot", "💊 Reminder", "🎯 Goals"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------- HOME ----------
if choice == "🏠 Home":
    st.write("Welcome to Healthcare Monitoring System")
    st.info("Track BP, BMI, get advice, chat & reminders")

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

# ---------- VIEW PATIENT ----------
elif choice == "📄 View Patient":
    st.subheader("Patient Details")

    pid = st.text_input("Enter Patient ID")
    data = load_data()

    if st.button("Search"):
        if pid in data:
            st.json(data[pid])

            # Graph
            st.subheader("Health Graph")
            st.bar_chart({
                "Systolic": [data[pid]["Systolic"]],
                "Diastolic": [data[pid]["Diastolic"]],
                "BMI": [data[pid]["BMI"]]
            })

            # Report
            if st.button("Generate Report"):
                report = f"""
Patient Report:
BP: {data[pid]["Systolic"]}/{data[pid]["Diastolic"]}
BMI: {data[pid]["BMI"]}
Advice: {data[pid]["Advice"]}
"""
                st.text(report)

            # CSV Download
            if st.button("Download CSV"):
                df = pd.DataFrame(data).T
                df.to_csv("health_data.csv")
                st.success("CSV file created")

        else:
            st.error("Patient not found")

# ---------- CHATBOT ----------
elif choice == "💬 Chatbot":
    st.subheader("Health Chatbot")

    question = st.text_input("Ask your question")

    if st.button("Ask"):
        q = question.lower()

        if "bp" in q:
            st.write("BP means Blood Pressure. Normal is 120/80.")
        elif "diet" in q:
            st.write("Eat fruits, vegetables, and avoid junk food.")
        elif "weight" in q:
            st.write("Exercise daily and maintain a healthy diet.")
        elif "exercise" in q:
            st.write("Do at least 30 minutes of exercise daily.")
        else:
            st.write("Consult a doctor for accurate advice.")

# ---------- REMINDER ----------
elif choice == "💊 Reminder":
    st.subheader("Medication Reminder")

    med = st.text_input("Medicine Name")
    time = st.time_input("Select Time")

    if st.button("Set Reminder"):
        st.success(f"Reminder set for {med} at {time}")

# ---------- GOALS ----------
elif choice == "🎯 Goals":
    st.subheader("Health Goal Setting")

    goal = st.text_input("Enter your goal")

    if st.button("Save Goal"):
        st.success("Goal saved successfully!")
    
  








