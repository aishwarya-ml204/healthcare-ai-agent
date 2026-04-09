import streamlit as st
import json
import pandas as pd

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


def simple_chatbot(q):
    q = q.lower()

    if "cause" in q and "bp" in q:
        return "High BP can be caused by stress, high salt intake, obesity, and lack of exercise."

    elif "control" in q and "bp" in q:
        return "To control BP, reduce salt, exercise daily, and avoid stress."

    elif "diet" in q and "overweight" in q:
        return "Eat fruits, vegetables, whole grains, and avoid fried foods."

    elif "exercise" in q:
        return "Do at least 30 minutes of exercise daily like walking or yoga."

    elif "bmi" in q:
        return "BMI is a measure of body fat based on height and weight."

    else:
        return "Please consult a doctor for proper advice."

  

# UI
st.title("🏥 Healthcare Monitoring AI Agent")

# Input
pid = st.text_input("Patient ID")
systolic = st.number_input("Systolic BP", min_value=0)
diastolic = st.number_input("Diastolic BP", min_value=0)
bmi = st.number_input("BMI", min_value=0.0)

#initialize history
if "history" not in st.session_state:
    st.session_state.history = []

advice = health_advice(systolic, diastolic, bmi)
# Save
if st.button("Save Data"):
    data = load_data()
    data[pid] = {
        "Systolic": systolic,
        "Diastolic": diastolic,
        "BMI": bmi,
        "Advice": advice
    }

    save_data(data)
    st.session_state.history.append({
        "Systolic": systolic,
        "Diastolic": diastolic,
        "BMI": bmi
    })

    st.success("✅ Data Saved!")
    st.write("Advice:", advice)
    if systolic > 140:
        st.error("⚠ High Blood Pressure Detected!")
    
if st.button("Generate Report"):
    st.subheader("📋 Health Report")
    st.write("Patient ID:", pid)
    st.write("BP:", systolic, "/", diastolic)
    st.write("BMI:", bmi)
    st.write("Advice:", advice)

st.subheader("💬 Ask AI Health Assistant")

query = st.text_input("Ask a health question", key="chat_input")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


query = st.text_input("Ask a health question")

if st.button("Ask AI", key="chatbot"):
    response = simple_chatbot(query)
    st.session_state.chat_history.append(("You", query))
    st.session_state.chat_history.append(("AI", response))
    st.write("### 💬 Chat History")

for role, msg in st.session_state.chat_history:
    st.write(f"**{role}:** {msg}")


# 💊 Medication Reminder
st.header("💊 Medication Reminder")

med_name = st.text_input("Medicine Name",key="med_name")
dosage = st.text_input("Dosage (e.g., 1 tablet)")
frequency = st.selectbox("Frequency", ["Once daily", "Twice daily"])
med_time = st.time_input("Select Time")

if "reminders" not in st.session_state:
    st.session_state.reminders = []

if st.button("Set Reminder", key="reminder"):
    reminder = f"{med_name} - {dosage} - {frequency} at {med_time}"
    st.session_state.reminders.append(reminder)
    st.success("Reminder saved!")


st.write("### 📋 Your Reminders")
for r in st.session_state.reminders:
    st.write(r)
    
 #medication interaction   
st.header("⚠ Check Medicine Interaction")

med1 = st.text_input("Enter Medicine 1", key="med1")
med2 = st.text_input("Enter Medicine 2",key="med2")

if st.button("Check Interaction"):
    if med1.lower() == "paracetamol" and med2.lower() == "alcohol":
        st.warning("⚠ Avoid taking paracetamol with alcohol")
    else:
        st.success("✅ No major interaction detected")
#health goal
st.header("🎯 Health Goal")

target_weight = st.number_input("Enter Target Weight")

if bmi > 25:
    st.write("⚠ You are overweight. Try to reach:", target_weight)
elif bmi < 18.5:
    st.write("⚠ You are underweight. Try to reach:", target_weight)
else:
    st.write("✅ You are healthy")
# -------------------------------
# History
# -------------------------------
st.write("### 📋 Patient History")
for h in st.session_state.history:
    st.write(h)
    
#graph
st.header("📊 Health Data Visualization")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.bar_chart(df)


# Disclaimer
st.markdown("---")
st.info("⚠ This app provides basic guidance. Consult a doctor for medical advice.")







