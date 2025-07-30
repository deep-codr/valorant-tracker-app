import streamlit as st
import pandas as pd
import json
import os

# Page config
st.set_page_config(page_title="Valorant Tracker", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #0f0f0f;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: #FF4655;
        }
        .footer {
            margin-top: 50px;
            text-align: center;
            font-size: 14px;
            color: gray;
        }
        .footer a {
            color: #ffffff;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>🎮 Valorant Match Tracker</h1>", unsafe_allow_html=True)
st.markdown("##### Enter your Riot ID below to fetch recent match stats.", unsafe_allow_html=True)

# Riot ID input
riot_id = st.text_input("🔍 Riot ID (e.g., varun#hub)")

# Load Data
if riot_id:
    filepath = f"data/riot_sample_data/{riot_id}.json"
    
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            match_data = json.load(f)
        st.success(f"📥 Data loaded for **{riot_id}**")

    else:
        sample_path = "data/riot_sample_data/sample.json"
        if os.path.exists(sample_path):
            with open(sample_path, "r") as f:
                match_data = json.load(f)
            st.warning(f"⚠️ No data found for `{riot_id}`. Showing sample data instead.")
        else:
            st.error("🚫 Sample data not found. Please add `sample.json` in `data/riot_sample_data/`.")
            st.stop()

    # Convert to DataFrame
    df = pd.DataFrame(match_data)

    # Safety Check: Column existence
    required_cols = ['kills', 'deaths', 'assists', 'win']
    if not all(col in df.columns for col in required_cols):
        st.error("❌ JSON file is missing required fields like 'kills', 'deaths', 'assists', 'win'.")
        st.stop()

    # Win Rate
    win_rate = round(df['win'].mean() * 100, 2)

    # Match Summary
    st.markdown("### 🧾 Match Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📊 Total Matches", len(df))
        st.metric("🔫 Avg Kills", round(df['kills'].mean(), 1))
    with col2:
        st.metric("💀 Avg Deaths", round(df['deaths'].mean(), 1))
        st.metric("🏆 Win Rate", f"{win_rate} %")

    # Line chart
    st.markdown("<h3 style='color:#FF4655;'>📈 Performance Over Matches</h3>", unsafe_allow_html=True)
    st.line_chart(df[['kills', 'deaths', 'assists']])

    # Full Data
    st.markdown("### 📋 Full Match Details")
    st.dataframe(df, use_container_width=True)

# Footer
st.markdown("""
    <div class='footer'>
        <hr style="margin-top: 40px; border-color: #FF4655;">
        <p>Made with ❤️ by <strong>Varun</strong> | Contact: <a href='mailto:respawncoder@gmail.com'>respawncoder@gmail.com</a></p>
        <p>© 2025 All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
