import streamlit as st
import json

file_name = "health_data.json"

# Load data
def load_data():
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except:
        return {}

# Save data
def save_data(data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

# Health advice logic
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

# UI
st.title("🏥 Healthcare Monitoring AI Agent")

# Input
pid = st.text_input("Patient ID")
systolic = st.number_input("Systolic BP", min_value=0)
diastolic = st.number_input("Diastolic BP", min_value=0)
bmi = st.number_input("BMI", min_value=0.0)

# Save
if st.button("Save Data"):
    data = load_data()

    advice = health_advice(systolic, diastolic, bmi)

    data[pid] = {
        "Systolic": systolic,
        "Diastolic": diastolic,
        "BMI": bmi,
        "Advice": advice
    }

    save_data(data)

    st.success("✅ Data Saved!")
    st.write("Advice:", advice)

import streamlit as st   # ✅ ADD THIS

def simple_chatbot(q):
    q = q.lower()

    if "cause" in q and "bp" in q:
        return "High BP can be caused by stress, high salt intake, lack of exercise, obesity, and genetics."
    elif "bp" in q:
        return "Blood pressure (BP) is the force of blood against artery walls."
    elif "overweight" in q:
        return "To manage weight, eat fruits, vegetables, whole grains and avoid junk food."
    elif "diet" in q:
        return "Healthy diet includes fruits, vegetables, proteins, and low sugar."
    elif "exercise" in q:
        return "Do at least 30 minutes of exercise daily like walking or yoga."
    else:
        return "Please consult a doctor for proper medical advice."

if st.button("Ask AI"):
    response = simple_chatbot(query)
    st.write(response)



# 💊 Medication Reminder
st.header("💊 Medication Reminder")

med_name = st.text_input("Enter Medicine Name")
med_time = st.time_input("Select Time")

if st.button("Set Reminder"):
    st.success(f"⏰ Reminder set for {med_name} at {med_time}")
    
