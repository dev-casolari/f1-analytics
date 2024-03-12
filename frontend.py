# FRONTEND

import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import fastf1 as f1

venue = st.selectbox("Select a venue", ["Bahrain"])
year = st.selectbox("Select a year", [2024])
session = st.selectbox("Select a session", ["Race"])


if st.button("Show"):

    with st.spinner('Loading data...'):
        race = f1.get_session(year, venue, session)
        race.load()
        laps = race.laps
        laps = laps[['Driver', 'LapTime', 'LapNumber', 'Stint', 'Compound', 'Team', 'TrackStatus', 'Position', 'Deleted', 'DeletedReason', 'IsAccurate']]
    
    st.session_state['laps'] = laps

if 'laps' in st.session_state:
    
    laps = st.session_state['laps']
    drivers = st.multiselect("Select drivers", list(laps['Driver'].unique()), max_selections=2)

    if len(drivers) == 2:
        st.session_state['drivers'] = drivers
    else:
        st.warning("Please select two drivers")
        st.session_state['drivers'] = None
        st.session_state.pop('drivers', None)


if 'drivers' in st.session_state:

    # driver = st.session_state['drivers'][0]
    # laps = st.session_state['laps']
    # laps = laps.reset_index(drop=True)
    # laps['LapTime'] = laps['LapTime'].dt.total_seconds()
    # laps['LapTime'] = laps.apply(lambda x: None if x['IsAccurate'] == False else x['LapTime'], axis=1)

    # driver_laps = laps.loc[laps['Driver'] == driver]
    # chart = alt.Chart(driver_laps).mark_line().encode(alt.Y('LapTime').scale(zero=False),
    #                                                   x='LapNumber',
    #                                                   color='Stint').properties(width=800, height=400)
    # st.altair_chart(chart)

    drivers = st.session_state['drivers']
    laps = st.session_state['laps']
    laps = laps.reset_index(drop=True)
    laps['LapTime'] = laps['LapTime'].dt.total_seconds()
    laps['LapTime'] = laps.apply(lambda x: None if x['IsAccurate'] == False else x['LapTime'], axis=1)

    for driver in drivers:
        driver_laps = laps.loc[laps['Driver'] == driver]
        chart = alt.Chart(driver_laps).mark_line().encode(alt.Y('LapTime').scale(zero=False),
                                                          x='LapNumber',
                                                          color='Stint').properties(width=800, height=400)
        st.altair_chart(chart)



