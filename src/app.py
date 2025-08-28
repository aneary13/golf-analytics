import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.calculations import (
    calculate_scoring_stats,
    calculate_driving_stats,
    calculate_approach_stats,
    calculate_short_game_stats,
    calculate_putting_stats,
)
from src.visualisations import (
    create_scoring_bar_chart,
    create_score_distribution_chart,
    create_driving_dispersion_chart,
    create_approach_dispersion_chart,
    create_putt_distribution_chart,
)

# --- Page Configuration ---
st.set_page_config(
    page_title="Golf Performance Dashboard",
    page_icon="⛳️",
    layout="wide"
)

# --- Main Application ---
st.title("⛳️ Golf Performance Analytics Dashboard")

# --- Load Data ---
# This function is cached, so it only runs when the data needs to be refreshed.
raw_df = load_data()

if raw_df.empty:
    st.warning("No data loaded. Please check your Google Sheet connection and data.")
else:
    # --- Sidebar Filters ---
    st.sidebar.header("Filters")
    
    # Filter by Course
    courses = raw_df['Course'].unique()
    selected_courses = st.sidebar.multiselect("Select Course(s)", courses, default=courses)
    
    # Filter by Date Range
    min_date = raw_df['Date'].min().date()
    max_date = raw_df['Date'].max().date()
    selected_date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Apply filters to the DataFrame
    filtered_df = raw_df[
        (raw_df['Course'].isin(selected_courses)) &
        (raw_df['Date'].dt.date >= selected_date_range[0]) &
        (raw_df['Date'].dt.date <= selected_date_range[1])
    ]

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # --- Calculate All Stats ---
        scoring_stats = calculate_scoring_stats(filtered_df)
        driving_stats = calculate_driving_stats(filtered_df)
        approach_stats = calculate_approach_stats(filtered_df)
        short_game_stats = calculate_short_game_stats(filtered_df)
        putting_stats = calculate_putting_stats(filtered_df)

        # --- Dashboard Layout (using tabs) ---
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Scoring", "Driving", "Approach", "Short Game", "Putting"])

        with tab1:
            st.header("Scoring Performance")
            col1, col2, col3 = st.columns(3)
            col1.metric("Avg Points per Hole", f"{scoring_stats.get('avg_stableford_points', 0):.2f}")
            col2.metric("Avg Strokes (Par 4)", f"{scoring_stats.get('avg_strokes_par_4', 0):.2f}")
            col3.metric("Avg Strokes (Par 5)", f"{scoring_stats.get('avg_strokes_par_5', 0):.2f}")
            
            st.plotly_chart(create_scoring_bar_chart(scoring_stats), use_container_width=True)
            
            st.subheader("Score Distribution")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.plotly_chart(create_score_distribution_chart(scoring_stats, 3), use_container_width=True)
            with c2:
                st.plotly_chart(create_score_distribution_chart(scoring_stats, 4), use_container_width=True)
            with c3:
                st.plotly_chart(create_score_distribution_chart(scoring_stats, 5), use_container_width=True)


        with tab2:
            st.header("Driving Performance")
            col1, col2, col3 = st.columns(3)
            col1.metric("FIR %", f"{driving_stats.get('fir_pct', 0):.1f}%")
            col2.metric("Ball in Play %", f"{driving_stats.get('ball_in_play_rate_pct', 0):.1f}%")
            col3.metric("Avg Distance", f"{driving_stats.get('avg_drive_distance', 0):.1f} yds")

            st.plotly_chart(create_driving_dispersion_chart(driving_stats), use_container_width=True)

        with tab3:
            st.header("Approach Performance")
            col1, col2 = st.columns(2)
            col1.metric("GIR %", f"{approach_stats.get('gir_pct', 0):.1f}%")
            col2.metric("Handicap GIR %", f"{approach_stats.get('handicap_gir_pct', 0):.1f}%")
            
            st.plotly_chart(create_approach_dispersion_chart(approach_stats), use_container_width=True)

        with tab4:
            st.header("Short Game Performance")
            col1, col2, col3 = st.columns(3)
            col1.metric("Scrambling %", f"{short_game_stats.get('scrambling_pct', 0):.1f}%")
            col2.metric("Handicap Scrambling %", f"{short_game_stats.get('handicap_scrambling_pct', 0):.1f}%")
            col3.metric("Short Game Score", f"{short_game_stats.get('short_game_score', 0):.2f}")

        with tab5:
            st.header("Putting Performance")
            col1, col2, col3 = st.columns(3)
            col1.metric("Avg Putts per Hole", f"{putting_stats.get('avg_putts_per_hole', 0):.2f}")
            col2.metric("3-Putt Avoidance %", f"{putting_stats.get('three_putt_avoidance_pct', 0):.1f}%")
            col3.metric("1-Putt %", f"{putting_stats.get('1_putt_pct', 0):.1f}%")
            
            st.plotly_chart(create_putt_distribution_chart(putting_stats), use_container_width=True)

            st.subheader("Diagnostic Stats")
            c1, c2 = st.columns(2)
            c1.metric("Avg Putts per GIR", f"{putting_stats.get('avg_putts_per_gir', 0):.2f}")
            c2.metric("Avg Putts per Missed GIR", f"{putting_stats.get('avg_putts_per_missed_gir', 0):.2f}")
