# FRONTEND

import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import fastf1 as f1


year = st.selectbox("Select a year", [2022, 2023, 2024])
st.session_state['year'] = year

if 'year' in st.session_state:
    year = st.session_state['year']
    schedule = f1.get_event_schedule(year)
    events = schedule['EventName'].unique()
    st.session_state['events'] = events

if 'events' in st.session_state:
    events = st.session_state['events']
    event = st.selectbox("Select a venue", events)
    st.session_state['event'] = event

    sessions = schedule.loc[schedule['EventName'] == event][['Session1', 'Session2', 'Session3', 'Session4', 'Session5']].values.tolist()
    sessions = [s for s in sessions[0] if s != 'None']
    st.session_state['sessions'] = sessions

if 'sessions' in st.session_state:

    sessions = st.session_state['sessions']
    session = st.selectbox("Select a session", sessions)
    st.session_state['session'] = session

if 'session' in st.session_state:
    year = st.session_state['year']
    event = st.session_state['event']
    session = st.session_state['session']

if st.button("Show") and 'session' in st.session_state:
    with st.spinner('Loading data...'):
        data = f1.get_session(year, event, session)
        data.load()
        st.session_state['data'] = data

if 'data' in st.session_state:
    data = st.session_state['data']

# add a separator
st.markdown("---")

if 'data' in st.session_state:
    # create a multibox to select drivers
    drivers = st.multiselect("Select drivers", list(data.laps['Driver'].unique()), max_selections=2)
    charts = []

    for driver in drivers:
        driver_laps = data.laps.loc[data.laps['Driver'] == driver]
        driver_laps = driver_laps.reset_index(drop=True)
        driver_laps['LapTime'] = driver_laps['LapTime'].dt.total_seconds()
        driver_laps['LapTime'] = driver_laps.apply(lambda x: None if x['IsAccurate'] == False else x['LapTime'], axis=1)
        st.write(driver)
        chart = alt.Chart(driver_laps).mark_line().encode(alt.Y('LapTime').scale(zero=False),
                                                          x='LapNumber',
                                                          color='Stint').properties(width=800, height=400)
        st.altair_chart(chart)
        charts.append(chart)






