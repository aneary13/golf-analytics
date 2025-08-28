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
raw_df = load_data()

if raw_df.empty:
    st.warning("No data loaded. Please check your Google Sheet connection and data.")
else:
    # --- Sidebar Filters ---
    st.sidebar.header("Filters")
    
    # Filter by Course
    courses = sorted(raw_df['Course'].unique())
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

    # Apply initial filters
    filtered_df = raw_df[
        (raw_df['Course'].isin(selected_courses)) &
        (raw_df['Date'].dt.date >= selected_date_range[0]) &
        (raw_df['Date'].dt.date <= selected_date_range[1])
    ]

    # --- Round Selection Filter ---
    st.sidebar.header("Round Selection")
    
    # Get unique rounds, sorted by date
    unique_rounds = filtered_df[['Round ID', 'Date']].drop_duplicates().sort_values(by='Date', ascending=False)
    
    filter_type = st.sidebar.selectbox(
        "Filter by Rounds",
        ["All Rounds", "Most Recent Rounds", "Best X of Last Y Rounds"]
    )

    final_df = filtered_df.copy()

    if filter_type == "Most Recent Rounds" and not unique_rounds.empty:
        num_recent = st.sidebar.number_input("Number of recent rounds", min_value=1, max_value=len(unique_rounds), value=min(3, len(unique_rounds)))
        recent_round_ids = unique_rounds.head(num_recent)['Round ID']
        final_df = filtered_df[filtered_df['Round ID'].isin(recent_round_ids)]

    elif filter_type == "Best X of Last Y Rounds" and not unique_rounds.empty:
        last_y = st.sidebar.number_input("Last Y rounds to consider", min_value=1, max_value=len(unique_rounds), value=min(20, len(unique_rounds)))
        best_x = st.sidebar.number_input("Best X rounds to select", min_value=1, max_value=last_y, value=min(8, last_y))
        
        # Get the last Y rounds
        last_y_round_ids = unique_rounds.head(last_y)['Round ID']
        last_y_df = filtered_df[filtered_df['Round ID'].isin(last_y_round_ids)]
        
        # Calculate average stableford points for each of these rounds and select the best (highest)
        round_scores = last_y_df.groupby('Round ID')['Score'].mean().nlargest(best_x)
        
        # Filter for the best X rounds
        best_round_ids = round_scores.index
        final_df = filtered_df[filtered_df['Round ID'].isin(best_round_ids)]


    if final_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # --- Calculate All Stats ---
        scoring_stats = calculate_scoring_stats(final_df)
        driving_stats = calculate_driving_stats(final_df)
        approach_stats = calculate_approach_stats(final_df)
        short_game_stats = calculate_short_game_stats(final_df)
        putting_stats = calculate_putting_stats(final_df)

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
