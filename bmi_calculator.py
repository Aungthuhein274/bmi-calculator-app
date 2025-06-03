import streamlit as st
import pandas as pd
import csv
import plotly.graph_objects as go

st.set_page_config(page_title="BMI Calculator", layout="centered")

# Title and description
st.title("BMI Calculator")
st.write("This is a simple calculator for BMI (Body Mass Index) related calculations.")
st.write("You can perform various calculations such as area, volume, and cost estimation.")


def calculate_bmi(height_m, weight_kg):
    if height_m > 0:
        return round(weight_kg / (height_m ** 2), 2)
    return None


def get_bmi_category(bmi):
    if bmi is None:
        return "Invalid"
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


def show_bmi_gauge(bmi):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi if bmi else 0,
        title={"text": "BMI"},
        gauge={
            "axis": {"range": [10, 40]},
            "bar": {"color": "blue"},
            "steps": [
                {"range": [0, 18.5], "color": "#b3c6e7"},
                {"range": [18.5, 24.9], "color": "#b6e7b3"},
                {"range": [25, 29.9], "color": "#ffe699"},
                {"range": [30, 40], "color": "#ffb3b3"}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)


def save_data(age, gender, height, weight, bmi, category):
    with open("bmi_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([age, gender, height, weight, bmi, category])


def load_data():
    try:
        data = pd.read_csv("bmi_data.csv", header=None, names=[
            "Age", "Gender", "Height", "Weight", "BMI", "Category"])
        return data
    except FileNotFoundError:
        return None


def clear_data():
    try:
        with open("bmi_data.csv", "w") as file:
            file.truncate(0)
        return True
    except FileNotFoundError:
        return False


# UI layout
col1, col2 = st.columns(2)
with col1:
    unit = st.selectbox("Select the unit of measurement:", [
        "Metric (cm/kg)", "Imperial (in/lb)"])
with col2:
    st.write("")
    st.write("")
    st.write("You can also convert between different units of measurement.")

# User input form
with st.form("bmi_form"):
    if unit == "Metric (cm/kg)":
        height = st.number_input(
            "Enter the height (cm):", min_value=0.0, step=0.1, help="Height in centimeters")
        weight = st.number_input(
            "Enter the weight (kg):", min_value=0.0, step=0.1, help="Weight in kilograms")
        height_m = height / 100
        weight_kg = weight
    else:
        height = st.number_input(
            "Enter the height (in):", min_value=0.0, step=0.1, help="Height in inches")
        weight = st.number_input(
            "Enter the weight (lb):", min_value=0.0, step=0.1, help="Weight in pounds")
        height_m = height * 0.0254
        weight_kg = weight * 0.453592
    age = st.number_input("Enter your age:", min_value=1,
                          max_value=110, step=1)
    gender = st.selectbox("Select your gender:", [
        "Prefer not to say", "Male", "Female"])
    submitted = st.form_submit_button("Calculate BMI")

if submitted:
    bmi = calculate_bmi(height_m, weight_kg)
    if bmi:
        st.subheader(f"Your BMI is: {bmi}")
        category = get_bmi_category(bmi)
        st.write(f"**Category:** {category}")
        if age < 18:
            st.info("As you are underaged, BMI should be interpreted with caution.")
        elif age <= 65:
            st.info("As an adult, BMI is a useful tool to assess your weight status.")
        if gender == "Male" and bmi > 25:
            st.warning(
                "BMI might overestimate body fat for muscular individuals.")
        show_bmi_gauge(bmi)
        st.markdown("---")
        col_save, col_load, col_clear, col_past = st.columns(4)
        with col_save:
            if st.button("Save Data"):
                save_data(age, gender, height, weight, bmi, category)
                st.success("Data saved successfully!")
        with col_load:
            if st.button("Load Data"):
                data = load_data()
                if data is not None:
                    st.write(data)
                else:
                    st.error("No data found. Please save data first.")
        with col_clear:
            if st.button("Clear Data"):
                if clear_data():
                    st.success("Data cleared successfully!")
                else:
                    st.error("No data found. Please save data first.")
        with col_past:
            if st.button("Past Results"):
                df = load_data()
                if df is not None:
                    st.dataframe(df)
                else:
                    st.error("No data found. Please save data first.")
    else:
        st.warning("Please enter a valid height and weight to calculate BMI.")
