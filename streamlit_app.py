import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Title for the app
st.title("Patient Follow-Up Analysis 👩‍🔬")

st.subheader("Easily Analyze Follow-Up Patients Data 📊")

st.write("""
Welcome to the Patient Follow-Up Analysis tool! Upload your file, and watch the magic happen as the tool automatically generates insightful graphs and trends. Just follow these simple instructions:

- **File Format**: Upload your data as an `.xlsx` file.
- **Column Names**: Ensure your file has these exact column names:
  - `patient id`
  - `Date`
  - `Follow Up`
- **Date Format**: Dates should follow the `dd/MM/YYYY` format.

Once you upload your data, the analysis will be displayed with automatically generated graphs. Enjoy exploring your insights!
""")

# Upload the Excel file
uploaded_file = st.file_uploader("Upload the Follow-Up Plans on Discharge Letters file", type="xlsx")
st.divider()
if uploaded_file is not None:
    # Load the data
    data = pd.read_excel(uploaded_file)
    
    # Display the data if needed
    st.subheader("Uploaded Data")
    st.write(data.head())
    
    # Analyzing the number of patients that need a follow-up
    follow_up_count = data['Follow Up'].value_counts()
    
    # Displaying the follow-up analysis
    st.subheader("Follow-Up Requirement Analysis")
    st.write(follow_up_count)
    fig_bar = px.bar(
        follow_up_count,
        x=follow_up_count.index,
        y=follow_up_count.values,
        labels={'x': 'Follow-Up Needed', 'y': 'Number of Patients'},
        title="Patients Requiring Follow-Up (Yes/No)",
        color=follow_up_count.index,
        color_discrete_sequence=['#1f77b4', '#ff7f0e']
    )
    st.plotly_chart(fig_bar)
    
    # Calculating daily trend of patients
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
        daily_trend = data.groupby(data['Date'].dt.date).size().reset_index(name='Number of Patients')
        
        # Plotting the trend with Plotly
        st.subheader("Daily Trend of Patients")
        fig_line = px.line(
            daily_trend,
            x='Date',
            y='Number of Patients',
            title="Daily Trend of Patients"
        )
        st.plotly_chart(fig_line)
    else:
        st.error("Date column not found in the uploaded file. Please check the data format.")
else:
    st.info("Please upload an Excel file to proceed.")
