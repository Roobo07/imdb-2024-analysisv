import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="IMDb 2024 Analytics", layout="wide")
st.title("🎬 IMDb 2024 Movie Explorer")

try:
    conn = sqlite3.connect("imdb_2024.db")
    df = pd.read_sql("SELECT * FROM movies_2024", conn)
    conn.close()

    # --- Sidebar Filters ---
    st.sidebar.header("Filter Results")
    
    # 1. Rating Filter
    rating_flt = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0)
    
    # 2. Voting Count Filter (The new requirement)
    # Using a number input allows for precise filtering like 10,000
    min_votes = st.sidebar.number_input("Minimum Voting Count", min_value=0, value=10000, step=1000)

    # Apply Filters to the Dataframe
    filtered_df = df[
        (df['Rating'] >= rating_flt) & 
        (df['Votes'] >= min_votes)
    ]

    # --- Metrics and Visuals ---
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Movies Found", len(filtered_df))
    
    st.subheader(f"Top Movies with > {min_votes:,} Votes")
    fig = px.scatter(filtered_df, x="Votes", y="Rating", 
                     size="Votes", hover_name="Title", 
                     color="Rating", title="Correlation: Votes vs Rating")
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Filtered Movie Data", filtered_df)

except Exception as e:
    st.error("Please run the scraper.py script first to generate the database!")