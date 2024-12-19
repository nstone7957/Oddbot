# File: requirements.txt
streamlit
pandas
requests
numpy

# File: streamlit_app.py
import streamlit as st
import pandas as pd
import time
import numpy as np
import requests

def get_odds(player_name, prop_type):
    """
    Placeholder function to get odds from different sportsbooks.
    Replace with actual API calls.
    """
    # Simulate different odds from various sportsbooks
    sportsbooks = {
        'DraftKings': {'odds': np.random.randint(-120, -100), 'line': round(np.random.uniform(20.5, 30.5), 1)},
        'FanDuel': {'odds': np.random.randint(-120, -100), 'line': round(np.random.uniform(20.5, 30.5), 1)},
        'BetMGM': {'odds': np.random.randint(-120, -100), 'line': round(np.random.uniform(20.5, 30.5), 1)},
        'Caesars': {'odds': np.random.randint(-120, -100), 'line': round(np.random.uniform(20.5, 30.5), 1)}
    }
    return sportsbooks

def main():
    st.set_page_config(page_title="Sports Odds Tracker", layout="wide")
    
    # Header
    st.title("🏀 Sports Odds Tracker")
    
    # Sidebar controls
    with st.sidebar:
        st.header("Settings")
        player_name = st.text_input("Player Name", "LeBron James")
        prop_type = st.selectbox("Prop Type", ["Points", "Rebounds", "Assists"])
        auto_refresh = st.checkbox("Auto-refresh")
        if auto_refresh:
            refresh_rate = st.slider("Refresh rate (seconds)", 30, 300, 60)

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("Check Odds") or auto_refresh:
            odds_data = get_odds(player_name, prop_type)
            
            # Convert to DataFrame for display
            df = pd.DataFrame(odds_data).T
            df.index.name = 'Sportsbook'
            
            # Display current odds
            st.subheader(f"Current {prop_type} Odds for {player_name}")
            st.dataframe(df.style.highlight_max(subset=['line'], color='lightgreen')
                                 .highlight_min(subset=['odds'], color='lightgreen'))
            
            # Find outliers
            lines = [data['line'] for data in odds_data.values()]
            max_diff = max(lines) - min(lines)
            
            if max_diff > 1:
                st.warning(f"⚠️ Found line differences of {max_diff} points!")
                
            # Show best values
            best_over = max(odds_data.items(), key=lambda x: x[1]['line'])
            best_under = min(odds_data.items(), key=lambda x: x[1]['line'])
            
            st.subheader("Best Available Lines")
            st.write(f"Best OVER: {best_over[0]} ({best_over[1]['line']} @ {best_over[1]['odds']})")
            st.write(f"Best UNDER: {best_under[0]} ({best_under[1]['line']} @ {best_under[1]['odds']})")

    with col2:
        st.subheader("Recent Changes")
        # Placeholder for tracking changes over time
        st.info("Historical tracking will appear here")
        
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(1)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
