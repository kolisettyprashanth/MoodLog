import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px

# Used Sheety API for data (Edit the URL if attaching a new file)
SHEETY_URL = "https://api.sheety.co/87b8eefb4cc926f74fd95f74044d124a/moodLog/sheet1"

st.set_page_config(page_title="Mood Logger", layout="centered")
st.title("🧪 Mood of the Queue")

#Adding logs for mood
st.header("Log a Mood")

mood = st.selectbox("How does the queue feel?", ["😊", "😠", "😕", "🎉"])
note = st.text_input("Add a short note (optional)")

if st.button("Submit"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "sheet1": {
            "timestamp": now,
            "mood": mood,
            "note": note
        }
    }

    res = requests.post(SHEETY_URL, json=payload)

    if res.status_code in [200, 201]:
        st.success("✅ Mood logged successfully!")
    else:
        st.error("❌ Something went wrong while submitting.")
        st.write("Status code:", res.status_code)
        st.write("Response:", res.text)

#Mood Chart
st.header("Mood Chart (Today)")

res = requests.get(SHEETY_URL)

if res.status_code == 200:
    try:
        records = res.json()['sheet1']
        df = pd.DataFrame(records)

        if df.empty:
            st.info("No mood entries yet.")
        else:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors="coerce")
            today = pd.Timestamp.now().normalize()
            df_today = df[df['timestamp'] >= today]

            if not df_today.empty:
                mood_counts = df_today['mood'].value_counts().reset_index()
                mood_counts.columns = ['Mood', 'Count']
                fig = px.bar(mood_counts, x='Mood', y='Count', title="Today's Mood Distribution")
                st.plotly_chart(fig)
            else:
                st.info("No moods logged today yet.")
    except Exception as e:
        st.error("⚠️ Error processing data.")
        st.write(e)
else:
    st.error("❌ Failed to fetch data from Google Sheets.")
    st.write("Status code:", res.status_code)
    st.write("Response:", res.text)

st.header("Mood Chart")

res = requests.get(SHEETY_URL)

if res.status_code == 200:
    try:
        records = res.json()['sheet1']
        df = pd.DataFrame(records)

        if df.empty:
            st.info("No mood entries yet.")
        else:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors="coerce")
            df['date'] = df['timestamp'].dt.date 
            df['time'] = df['timestamp'].dt.time  

            # Filter by date
            unique_dates = sorted(df['date'].unique(), reverse=True)
            selected_date = st.selectbox("Select a date", unique_dates, index=0)

            # Filter by mood 
            unique_moods = df['mood'].unique().tolist()
            selected_moods = st.multiselect("Filter by mood(s)", unique_moods, default=unique_moods)

            # Apply filters
            df_filtered = df[(df['date'] == selected_date) & (df['mood'].isin(selected_moods))]

            if df_filtered.empty:
                st.info("No moods logged with this filter.")
            else:
                mood_counts = df_filtered['mood'].value_counts().reset_index()
                mood_counts.columns = ['Mood', 'Count']
                fig = px.bar(mood_counts, x='Mood', y='Count', title=f"Mood Distribution for {selected_date}")
                st.plotly_chart(fig)

    except Exception as e:
        st.error("⚠️ Error processing data.")
        st.write(e)
else:
    st.error("❌ Failed to fetch data from Google Sheets.")
    st.write("Status code:", res.status_code)
    st.write("Response:", res.text)
