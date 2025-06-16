import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>📊 Homelessness Data Dashboard - Ireland</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Interactive dashboard for policy makers to analyse homelessness data across Irish regions</p>", unsafe_allow_html=True)

# --- Load Data ---
data = pd.read_csv("homelessness-report-march-2025.csv")

# --- Sidebar Filters ---
st.sidebar.header("Filter Data")
region = st.sidebar.selectbox("Select Region", options=["All"] + list(data['Region'].unique()))

# --- Apply Region Filter ---
data_filtered = data.copy()
if region != "All":
    data_filtered = data_filtered[data_filtered["Region"] == region]

# --- KPI Cards ---
total_adults_all = data['Total Adults'].sum()
total_families_all = data['Number of Families'].sum()
total_dependants_all = data['Number of Dependants in Families'].sum()

total_adults_filtered = data_filtered['Total Adults'].sum()
total_families_filtered = data_filtered['Number of Families'].sum()
total_dependants_filtered = data_filtered['Number of Dependants in Families'].sum()

def get_trend_icon(current, total):
    if current > total:
        return "<span style='color:green; font-size:14px;'>▲</span>"
    elif current < total:
        return "<span style='color:red; font-size:14px;'>▼</span>"
    else:
        return "<span style='color:gray; font-size:14px;'>●</span>"

st.markdown("## Key Statistics")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown(f"""
        <div style='padding: 15px; background-color: #ffffff; border: 1px solid #ddd; border-radius: 10px;'>
            <div style='font-size: 16px; color: #555;'>Total Homeless Adults</div>
            <div style='font-size: 26px; color: #111;'>{total_adults_filtered:,} {get_trend_icon(total_adults_filtered, total_adults_all)}</div>
        </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
        <div style='padding: 15px; background-color: #ffffff; border: 1px solid #ddd; border-radius: 10px;'>
            <div style='font-size: 16px; color: #555;'>Total Families</div>
            <div style='font-size: 26px; color: #111;'>{total_families_filtered:,} {get_trend_icon(total_families_filtered, total_families_all)}</div>
        </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
        <div style='padding: 15px; background-color: #ffffff; border: 1px solid #ddd; border-radius: 10px;'>
            <div style='font-size: 16px; color: #555;'>Total Dependants</div>
            <div style='font-size: 26px; color: #111;'>{total_dependants_filtered:,} {get_trend_icon(total_dependants_filtered, total_dependants_all)}</div>
        </div>
    """, unsafe_allow_html=True)

# --- Gender Distribution ---
gender_data = data_filtered.copy()
gender_data["Male %"] = gender_data["Male Adults"] / gender_data["Total Adults"] * 100
gender_data["Female %"] = gender_data["Female Adults"] / gender_data["Total Adults"] * 100
fig_gender = px.bar(gender_data, x="Region", y=["Male %", "Female %"], barmode="stack", title="Homeless Population Gender Distribution by Region (%)")
st.plotly_chart(fig_gender, use_container_width=True)

# --- Age Group ---
st.subheader("Breakdown of Homeless Adults by Age Group")
age_group = st.radio("Select Chart Type", ["Bar", "Pie"], horizontal=True)
age_totals = {
    "18-24": data_filtered["Adults Aged 18-24"].sum(),
    "25-44": data_filtered["Adults Aged 25-44"].sum(),
    "45-64": data_filtered["Adults Aged 45-64"].sum(),
    "65+": data_filtered["Adults Aged 65+"].sum(),
}
if age_group == "Bar":
    fig_age = px.bar(x=list(age_totals.keys()), y=list(age_totals.values()), labels={'x': 'Age Group', 'y': 'Total Adults'}, title="Adults by Age Group")
else:
    fig_age = px.pie(values=list(age_totals.values()), names=list(age_totals.keys()), title="Adults by Age Group")
st.plotly_chart(fig_age, use_container_width=True)

# --- Accommodation Access ---
accom_data = {
    "Private Emergency": data_filtered["Number of people who accessed Private Emergency Accommodation"].sum(),
    "Supported Temporary": data_filtered["Number of people who accessed Supported Temporary Accommodation"].sum(),
    "Temporary Emergency": data_filtered["Number of people who accessed Temporary Emergency Accommodation"].sum(),
    "Other": data_filtered["Number of people who accessed Other Accommodation"].sum()
}
fig_accom = px.bar(x=list(accom_data.keys()), y=list(accom_data.values()), title="Accommodation Access Types", labels={'x': 'Accommodation Type', 'y': 'People'})
st.plotly_chart(fig_accom, use_container_width=True)

# --- Family Composition ---
family_data = {
    "Families": data_filtered["Number of Families"].sum(),
    "Adults in Families": data_filtered["Number of Adults in Families"].sum(),
    "Single-Parent Families": data_filtered["Number of Single-Parent families"].sum(),
    "Dependants": data_filtered["Number of Dependants in Families"].sum()
}
fig_family = px.bar(x=list(family_data.keys()), y=list(family_data.values()), title="Family Composition", labels={'x': 'Family Category', 'y': 'Total Count'})
st.plotly_chart(fig_family, use_container_width=True)

# --- Regional Distribution ---
if region == "All":
    st.subheader("Regional Distribution of Homeless Adults")
    adult_chart = px.bar(data, x="Region", y="Total Adults", color="Region", title="Total Adults by Region")
    st.plotly_chart(adult_chart, use_container_width=True)

# --- Citizenship Distribution (Interactive) ---
st.subheader("Distribution by Citizenship")
chart_type = st.radio("Select Chart Type", ["Pie", "Bar"], horizontal=True)

citizenship_data = {
    "Irish": data_filtered["Number of people with citizenship Irish"].sum(),
    "EEA/UK": data_filtered["Number of people with citizenship EEA/Uk"].sum(),
    "Non-EEA": data_filtered["Number of people with citizenship Non-EEA"].sum()
}

if chart_type == "Pie":
    fig_citizenship = px.pie(
        names=list(citizenship_data.keys()),
        values=list(citizenship_data.values()),
        title="Homeless Adults by Citizenship"
    )
else:
    fig_citizenship = px.bar(
        x=list(citizenship_data.keys()),
        y=list(citizenship_data.values()),
        title="Homeless Adults by Citizenship",
        labels={'x': 'Citizenship', 'y': 'Count'}
    )

st.plotly_chart(fig_citizenship, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("<center><i>Developed for Government Public Policy Review | Built by Saad Khan using Streamlit & Plotly</i></center>", unsafe_allow_html=True)
