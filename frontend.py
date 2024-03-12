# FRONTEND

import matplotlib.pyplot as plt
import streamlit as st
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
    
    drivers = st.multiselect("Select drivers", list(laps['Driver'].unique()), max_selections=2)

if len(drivers) == 0:
    st.error("Please select at least one driver")
else:
    st.write(f"Selected drivers: {drivers}")

    dr1 = drivers[0]
    dr2 = drivers[1]

    dr1_laps = laps.loc[laps['Driver']==dr1]
    dr2_laps = laps.loc[laps['Driver']==dr2]

    dr1_laps.reset_index(drop=True, inplace=True)
    dr2_laps.reset_index(drop=True, inplace=True)

    dr1_laps['LapTime'] = dr1_laps['LapTime'].apply(lambda x: x.total_seconds())
    dr2_laps['LapTime'] = dr2_laps['LapTime'].apply(lambda x: x.total_seconds())

    dr1_laps['LapTime'] = dr1_laps.apply(lambda x: None if x['IsAccurate']==False else x['LapTime'], axis=1)
    dr2_laps['LapTime'] = dr2_laps.apply(lambda x: None if x['IsAccurate']==False else x['LapTime'], axis=1)

    st.line_chart(dr1_laps['LapTime'])
    st.line_chart(dr2_laps['LapTime'])

