import streamlit as st
import pandas as pd
import csv
import plotly.graph_objects as go

st.set_page_config(page_title="BMI Calculator", layout="centered")

# Title and description
st.title("BMI Calculator")
st.write("This is a simple calculator for BMI (Body Mass Index) related calculations.")
st.write("You can perform various calculations such as area, volume, and cost estimation.")

# Unit conversion selection
unit = st.selectbox("Select the unit of measurement:", [
                    "Metric (cm/kg)", "Imperial (in/lb)"])
st.write("You can also convert between different units of measurement.")

# Input fields
if unit == "Metric (cm/kg)":
    height = st.number_input("Enter the height (cm):", min_value=0.0, step=0.1)
    weight = st.number_input("Enter the weight (kg):", min_value=0.0, step=0.1)
    height_m = height / 100
    weight_kg = weight
else:
    height = st.number_input("Enter the height (in):", min_value=0.0, step=0.1)
    weight = st.number_input("Enter the weight (lb):", min_value=0.0, step=0.1)
    height_m = height * 0.0254
    weight_kg = weight * 0.453592

# Additional inputs
age = st.number_input("Enter your age:", min_value=1, max_value=110, step=1)
gender = st.selectbox("Select your gender:", [
                      "Prefer not to say", "Male", "Female"])

# BMI Calculation
if height_m > 0:
    bmi = round(weight_kg / (height_m ** 2), 2)
    st.subheader(f"Your BMI is: {bmi}")

    # BMI categories
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
    st.write(f"**Category:** {category}")

    # Age and gender based advice
    if age < 18:
        st.info("As you are underaged, BMI should be interpreted with caution.")
    elif age <= 65:
        st.info("As an adult, BMI is a useful tool to assess your weight status.")
    if gender == "Male" and bmi > 25:
        st.warning("BMI might overestimate body fat for muscular individuals.")

    # Plotting
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        title={"text": "BMI"},
        gauge={
            "axis": {"range": [10, 40]},
            "bar": {"color": "blue"},
            "steps": [
                {"range": [0, 18.5], "color": "lightblue"},
                {"range": [18.5, 24.9], "color": "lightgreen"},
                {"range": [25, 29.9], "color": "yellow"},
                {"range": [30, 40], "color": "red"}
            ]
        }
    ))
    st.plotly_chart(fig)

    # Save data
    if st.button("Save Data"):
        with open("bmi_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([age, gender, height, weight, bmi, category])
            st.success("Data saved successfully!")

    # Load data
    if st.button("Load Data"):
        try:
            data = pd.read_csv("bmi_data.csv", header=None, names=[
                               "Age", "Gender", "Height", "Weight", "BMI", "Category"])
            st.write(data)
        except FileNotFoundError:
            st.error("No data found. Please save data first.")

    # Clear data
    if st.button("Clear Data"):
        try:
            with open("bmi_data.csv", "w") as file:
                file.truncate(0)
            st.success("Data cleared successfully!")
        except FileNotFoundError:
            st.error("No data found. Please save data first.")

    # Past results
    if st.button("Past Results"):
        try:
            df = pd.read_csv("bmi_data.csv", header=None, names=[
                             "Age", "Gender", "Height", "Weight", "BMI", "Category"])
            st.dataframe(df)
        except FileNotFoundError:
            st.error("No data found. Please save data first.")
else:
    st.warning("Please enter a valid height and weight to calculate BMI.")
