import streamlit as st
import pandas as pd
import time
from statsbombpy import sb

# Set page config
st.set_page_config(page_title="Football Data Analysis", layout="wide")

# Configure cache for API calls
@st.cache_data
def get_competition_matches():
    """Get all Women's Euro 2022 matches"""
    competitions = sb.competitions()
    # Filter for Women's Euro 2022
    euro22 = competitions[(competitions['competition_name'] == "UEFA Women's Euro") & 
                          (competitions['season_name'] == "2022")]
    
    if len(euro22) > 0:
        comp_id = euro22.iloc[0]['competition_id']
        season_id = euro22.iloc[0]['season_id']
        matches = sb.matches(comp_id, season_id)
        return matches
    return None

@st.cache_data
def get_match_events(match_id: int):
    """Get events for a specific match"""
    return sb.events(match_id=match_id)

@st.cache_data
def get_match_lineups(match_id: int):
    """Get lineups for a specific match"""
    return sb.lineups(match_id=match_id)

# Load matches and create lookup
try:
    matches_df = get_competition_matches()
    if matches_df is not None:
        # Create match lookup dictionary
        matches_df
        EURO22MATCHES = {}
        for _, row in matches_df.iterrows():
            match_name = f"{row['home_team'].replace(' Women\'s', '')} vs {row['away_team'].replace(' Women\'s', '')}"
            EURO22MATCHES[match_name] = row['match_id']
    else:
        st.error("Could not load Women's Euro 2022 matches")
        EURO22MATCHES = {}
except Exception as e:
    st.error(f"Error loading matches: {e}")
    EURO22MATCHES = {}

st.title("⚽ Football Data Analysis")

# Initialize session state
if 'task_1_start_time' not in st.session_state:
    st.session_state.task_1_start_time = None
if 'task_1_submitted' not in st.session_state:
    st.session_state.task_1_submitted = False
if 'task_1_time' not in st.session_state:
    st.session_state.task_1_time = None

# Title and Introduction
st.markdown("""
Identifying Fast Passers Using Data

[Women's Euros 2022 - England vs Norway](https://www.youtube.com/watch?v=EAdTGBRSCEQ)

- When should I substitute a player?
- What training should focus on for the next game?
""")

##st.video("https://www.youtube.com/watch?v=EAdTGBRSCEQ")


# Task 1 Section
st.header("Task 1: Right Footed Goals in England vs Norway")

col1, col2 = st.columns(2)

with col1:
    if st.button("Start Timer - Watch the highlights"):
        st.session_state.task_1_start_time = time.time()
        st.session_state.task_1_submitted = False
        st.info("Timer started! Watch the highlights and count the Right Footed Goals.")

with col2:
    if st.session_state.task_1_start_time is not None and not st.session_state.task_1_submitted:
        elapsed = int(time.time() - st.session_state.task_1_start_time)
        st.metric("Elapsed Time", f"{elapsed}s")

st.markdown("""
**Instructions:**
1. Click "Start Timer" above
2. Watch the highlights video (not the whole match)
3. Note down the body part used to score each goal
4. Input the "Number of Right Footed Goals" below
5. Click "Submit Answer"
""")

right_footed_input = st.number_input("Number of Right Footed Goals:", min_value=0, step=1)

if st.button("Submit Answer - Task 1"):
    if st.session_state.task_1_start_time is not None:
        st.session_state.task_1_time = time.time() - st.session_state.task_1_start_time
        st.session_state.task_1_submitted = True
        
        st.success(f"Submitted! You took {int(st.session_state.task_1_time)} seconds")
        
        clips_length_in_seconds = 97
        match_length_in_seconds = 95.0 * 60
        
        st.info(f"It would take at least {int(((st.session_state.task_1_time / clips_length_in_seconds) * match_length_in_seconds) / 60)} minutes to do this for the whole match")

st.divider()

# Example Analysis: Using Data
st.header("Example: How many Right Footed goals using Data?")

if st.button("Analyze England vs Norway data"):
    try:
        with st.spinner("Fetching data..."):
            match_id = EURO22MATCHES.get('England vs Norway')
            if match_id is None:
                st.error("Match 'England vs Norway' not found")
            else:
                events_df = get_match_events(match_id)
                
                # Filter for goals
                goals = events_df[(events_df['type'] == 'Shot') & 
                                (events_df['shot_outcome'] == 'Goal')]
                
                # Count right footed goals
                right_footed_goals = len(goals[goals['shot_body_part'] == 'Right Foot'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Right Footed Goals (from data)", right_footed_goals)
                
                st.subheader("Goal Details:")
                display_df = goals[['timestamp', 'period', 'shot_body_part', 'shot_outcome']].copy()
                st.dataframe(display_df.reset_index(drop=True))
    except Exception as e:
        st.error(f"Error fetching data: {e}")

st.divider()

# Task 2 Section
st.header("Task 2: Headed Goals in England vs Sweden")

st.markdown("""
**Analyze the data:**
1. Use the data for the "England vs Sweden" game
2. Filter for "Head" goals instead of "Right Foot"
3. Click "Analyze" to see results
""")

if st.button("Analyze England vs Sweden data"):
    try:
        with st.spinner("Fetching data..."):
            match_id = EURO22MATCHES.get('England vs Sweden')
            if match_id is None:
                st.error("Match 'England vs Sweden' not found")
            else:
                events_df = get_match_events(match_id)
                
                # Filter for goals
                goals = events_df[(events_df['type'] == 'Shot') & 
                                (events_df['shot_outcome'] == 'Goal')]
                
                # Count headed goals
                headed_goals = len(goals[goals['shot_body_part'] == 'Head'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Headed Goals in Sweden game", headed_goals)
                
                st.subheader("Goal Details:")
                display_df = goals[['timestamp', 'period', 'shot_body_part', 'shot_outcome']].copy()
                st.dataframe(display_df.reset_index(drop=True))
    except Exception as e:
        st.error(f"Error fetching data: {e}")

st.divider()

# Extension Section
st.header("Extension: Shots Analysis")

st.markdown("""
**Analyze all shots in the Netherlands vs Sweden game**

Including: player, team, and shot technique
""")

if st.button("Analyze Netherlands vs Sweden shots"):
    try:
        with st.spinner("Fetching data..."):
            match_id = EURO22MATCHES.get('Netherlands vs Sweden')
            if match_id is None:
                st.error("Match 'Netherlands vs Sweden' not found")
            else:
                events_df = get_match_events(match_id)
                
                # Filter for shots
                shots = events_df[events_df['type'] == 'Shot']
                
                st.metric("Total Shots", len(shots))
                
                st.subheader("All Shots Details:")
                display_cols = ['timestamp', 'period', 'player', 'team', 'shot_technique', 'shot_outcome', 'shot_body_part']
                available_cols = [col for col in display_cols if col in shots.columns]
                st.dataframe(shots[available_cols].reset_index(drop=True))
    except Exception as e:
        st.error(f"Error fetching data: {e}")

st.divider()

# Footer
st.markdown("""
---
**Data Source:** [StatsBomb](https://statsbomb.com/) - Women's Euro 2022 Free Data
""")
