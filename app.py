import streamlit as st
import pandas as pd
import json
import plotly.express as px
import matplotlib.pyplot as plt

st.title("HFLAV - B to Charm")

with open('gsoc_hflav.json') as f:
    data = json.load(f)

col_list = ["Decay Particle", "Average", "Total Error", "Measurement Errors", "Measurement Values"]
total_data = pd.read_csv('hflv.csv', usecols=col_list)

st.sidebar.title("choose settings")
st.sidebar.write("(For first graph)")

all_particle_names = list(total_data.columns.unique())
col_x = st.sidebar.selectbox("choose first parameter", all_particle_names)
col_y = st.sidebar.selectbox("choose second parameter", all_particle_names)

st.sidebar.header("select visualization type")
select = st.sidebar.selectbox("Options", ["Heatmap", "Bar Chart", "Log Chart"], key=2)

st.header("choose settings from the sidebar")

if select == "Heatmap":
    fig = px.density_heatmap(total_data, x = col_x, y = col_y)
    st.plotly_chart(fig)
elif select == "Bar Chart":
    fig = px.bar(total_data, x = col_x, y = col_y)
    st.plotly_chart(fig)
else:
    fig = px.scatter(total_data, x = col_x, y = col_y, log_x=True)
    st.plotly_chart(fig)

st.sidebar.title("Measurements")
st.sidebar.write("(For second graph)")
st.header("Select measurement type to compare")

def get_values():
    for key in data['keys']:
        measurements = key['measurements']
        for value_data in measurements:
            values = value_data['value']
            save_values.append(values)

save_values = []
get_values()

def get_errors():
    for key in data['keys']:
        measurements = key['measurements']
        for error_data in measurements:
            errors = error_data['error']
            save_errors.append(errors)

save_errors = []
get_errors()

for key in data['keys']:
    del(key['latex'])

value_select = st.sidebar.checkbox("values", save_values)
error_select = st.sidebar.checkbox("errors", save_errors)

second_arg = st.sidebar.selectbox("choose second argument", all_particle_names)

if value_select:
    select_visualizer = st.sidebar.selectbox("select visualizer", ["Bar Chart", "Pie Chart", "Heatmap"], key=2)
    if select_visualizer == "Bar Chart":
        fig = px.bar(total_data, x = second_arg, y = get_values())
        st.plotly_chart(fig)
    elif select_visualizer == "Heatmap":
        fig = px.density_heatmap(total_data, x = second_arg, y = get_values())
        st.plotly_chart(fig)
    else:
        fig = px.pie(total_data, values = second_arg, names = get_values())
        st.plotly_chart(fig)
else:
    select_visualizer = st.sidebar.selectbox("select visualizer", ["Bar Chart", "Pie Chart", "Heatmap"], key=2)
    if select_visualizer == "Bar Chart":
        fig = px.bar(total_data, x = second_arg, y = get_errors())
        st.plotly_chart(fig)
    elif select_visualizer == "Heatmap":
        fig = px.density_heatmap(total_data, x = second_arg, y = get_errors())
        st.plotly_chart(fig)
    else:
        fig = px.pie(total_data, values = second_arg, names = get_errors())
        st.plotly_chart(fig)


