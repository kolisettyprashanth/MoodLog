# Mood Log

This is a simple internal tool for logging and visualizing the mood of a patient support ticket queue throughout the day.

---

## Features

- Log a mood via emoji dropdown with optional note  
- Store entries in a Google Sheet via Sheety API  
- Visualize mood counts for selected dates and moods using an interactive bar chart  
- Filter mood data by day and mood type  
- Built with Python, Streamlit, Pandas, Requests, and Plotly  

---

## Setup

### Prerequisites

- Python 3.7+  
- Google Sheet connected with Sheety API  
- Streamlit installed (`pip install streamlit`)

### Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/kolisettyprashanth/MoodLog.git
   cd mood-tracker
2. Update the Sheety URL in app.py
3. Run the app: streamlit run app.py
