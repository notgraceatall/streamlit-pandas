import os
import streamlit as st
import pandas as pd
import time
from statsbombpy import sb

# py -m pip install streamlit statsbombpy pandas
# py -m streamlit run demos.py


# Getting a dataframe

# df = pd.read_excel("planets.xlsx")
# df = pd.read_sql_table("planets", "sqlite:///planets.db")
# df = pd.read_json("planets.json")
# df = pd.read_csv("demo.cvs")

# 
df = sb.events(match_id=3835331)

st.title("Streamlit Demos :)")

# Calculating a field
df['time_seconds'] = pd.to_timedelta(df['timestamp']).dt.total_seconds()
df = df[(df['time_seconds'] >= 0) & (df['time_seconds'] <= 4000)]

# Trim down to just the fields we want
df = df[['timestamp', 'time_seconds', 'period', 'player', 'team', 'type',
         'location', 'duration', 'shot_body_part', 'shot_deflected',
         'shot_end_location', 'shot_first_time', 'shot_one_on_one',
         'shot_outcome', 'shot_saved_off_target', 'shot_statsbomb_xg',
         'shot_technique', 'shot_type']]

df # Shows the dataframe in the Streamlit app


# Saving cleaned data to a new file
if "output" not in os.listdir():
    os.mkdir("output")

df.to_csv("output/shot_position.csv", index=False)
df.to_excel("output/shot_position.xlsx", index=False)
df.to_json("output/shot_position.json", orient="records")

st.subheader("Example - Filtering")

st.text("""Here we filter the data to just shots that were first time shots 
        (i.e. not rebounds or shots taken after a dribble).""")
shots_first_time_df = df[(df['type']=="Shot") & (df['shot_first_time'] == True )]
shots_first_time_df


st.text("""Volley and half volley shots.
Can be said as the shot_technique being either "Volley" or "Half Volley".""")
shots_volley_df = df[(df['shot_technique'].isin(["Half Volley","Volley"]))]
shots_volley_df

st.text("""Long Carrys (dribbles) can be defined as events where the duration
        is greater than 10 seconds and the type is "Carry".""")
long_dribble_df = df[(df['duration'] > 10 ) & (df['type'] == "Carry" )]
long_dribble_df


st.subheader("Grouping")
team_stats = df.groupby('team')['shot_statsbomb_xg'].agg(['sum', 'mean', 'count']).reset_index()
team_stats.columns = ['team', 'total_xg', 'average_xg', 'shot_count']   
team_stats


st.subheader("Shot Counts by Player")

player_shots = df['player'].value_counts().reset_index()
player_shots.columns = ['player', 'shot_count'] 

player_shots

st.subheader("Filtering")

event_period = st.selectbox("Select event period", ["1","2"])   

# Filter where data is equal to the selected value
df = df[df['period'] == int(event_period)]

# Slider Range
st.subheader("Filter by Slider")
start, end = st.slider("Filter by event time (seconds)", min_value=0,
                               max_value=int(df['time_seconds'].max()), 
                               value=(0, int(df['time_seconds'].max())),
                               step=10)

# Filter where value is between the start and end values
df = df[(df['time_seconds'] >= start) & (df['time_seconds'] <= end)]

# Dropdown list of body parts
st.subheader("Filter by Select Box")
body_part = st.selectbox("Select body part", ["Left Foot", "Right Foot", "Head", "Other"])
try :
    df = df[df['shot_body_part'] == body_part]
except:
    st.warning("No shots found for the selected body part.")
    
    
df # Shows the filtered dataframe in the Streamlit app


