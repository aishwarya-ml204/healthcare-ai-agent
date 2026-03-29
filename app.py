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
st.title("🏥 Healthcare AI Assistant")

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
