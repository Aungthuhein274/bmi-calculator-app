# BMI Calculator (Streamlit)

A modern, interactive BMI (Body Mass Index) calculator built using Python and Streamlit.

Features
--------
- Unit conversation ( Metric and Imperial )
- Personalized Feedback: Age and gender-based BMI advice.
- Interactive Visualization: BMI gauge chart powered by Plotly.
- History Tracking: Save, view, and clear your BMI records (CSV-based).
- Instant Results: All calculations and charts update live.

Getting Started
---------------

Prerequisites:
- Python 3.10+
- pip

Installation:
Install dependencies:

    pip install streamlit pandas plotly

Run the App:

    streamlit run bmi_calculator.py

Usage
-----
- Select your preferred unit system (Metric or Imperial).
- Enter your height, weight, age, and gender.
- Click Calculate BMI to see your result, category, and advice.
- Use the buttons to save, load, clear, or view past BMI records.

About BMI
---------
BMI is a simple index of weight-for-height commonly used to classify underweight, normal weight, overweight, and obesity in adults. For children and teens, BMI should be interpreted with caution.

Data Storage
------------
- All BMI records are saved in a local CSV file (bmi_data.csv).
- You can clear or reload your history at any time from the app interface.

License
-------
This project is open-source and free to use for personal and educational purposes.
Developed By : Aung Thu Hein (Lethean Joel)