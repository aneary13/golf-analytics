import pandas as pd
import pytest

from src.calculations import (
    calculate_approach_stats,
    calculate_driving_stats,
    calculate_putting_stats,
    calculate_scoring_stats,
    calculate_short_game_stats,
)


@pytest.fixture
def sample_clean_df():
    """
    Provides a small, cleaned DataFrame for testing calculation functions.
    This data is structured as if it has already been processed by data_loader.
    """
    data = {
        "Par": [4, 3, 4, 5, 4, 5],
        "Strokes": [4, 3, 7, 5, 4, 7],
        "Score": [3, 3, 1, 2, 2, 1],
        "Shots": [2, 1, 1, 2, 1, 2],  # Handicap shots
        "FIR": [1, None, 0, 1, 1, 0],
        "Tee Shot Location": [
            "Fairway",
            None,
            "Right",
            "Fairway",
            "Fairway",
            "OB Right",
        ],
        "Tee Shot Distance": [200, None, 220, 250, 210, 230],
        "GIR": [0, 1, 0, 1, 1, 0],
        "Approach Location": ["Short", "Green", "Right", "Green", "Green", "Long"],
        "Putts": [1, 1, 2, 2, 1, 3],
        "Shots Inside 100y": [1, 0, 2, 0, 0, 2],
    }
    df = pd.DataFrame(data)
    return df


def test_calculate_scoring_stats(sample_clean_df):
    """
    Tests the calculate_scoring_stats function with a sample DataFrame.
    """
    stats = calculate_scoring_stats(sample_clean_df)
    assert stats["avg_strokes_par_3"] == 3.00
    assert stats["avg_strokes_par_4"] == 5.00
    assert stats["avg_strokes_par_5"] == 6.00
    assert pytest.approx(stats["avg_stableford_points"]) == 2.0


def test_calculate_driving_stats(sample_clean_df):
    """
    Tests the calculate_driving_stats function with a sample DataFrame.
    """
    stats = calculate_driving_stats(sample_clean_df)
    assert stats["fir_pct"] == 60.0
    assert stats["ball_in_play_rate_pct"] == 80.0
    assert stats["dispersion"]["Fairway"] == 60.0
    assert stats["avg_drive_distance"] == 222.0


def test_calculate_approach_stats(sample_clean_df):
    """
    Tests the calculate_approach_stats function with a sample DataFrame.
    """
    stats = calculate_approach_stats(sample_clean_df)
    assert stats["gir_pct"] == 50.0
    assert stats["handicap_gir_pct"] == pytest.approx(83.33, 0.01)
    assert stats["approach_dispersion"]["Green"] == 50.0


def test_calculate_short_game_stats(sample_clean_df):
    """
    Tests the calculate_short_game_stats function with a sample DataFrame.
    """
    stats = calculate_short_game_stats(sample_clean_df)
    assert stats["avg_strokes_to_green_inside_100y"] == pytest.approx(1.67, 0.01)
    assert stats["scrambling_pct"] == pytest.approx(33.33, 0.01)
    assert stats["handicap_scrambling_pct"] == 0.0
    assert stats["short_game_score"] == pytest.approx(3.67, 0.01)


def test_calculate_putting_stats(sample_clean_df):
    """
    Tests the calculate_putting_stats function with a sample DataFrame.
    """
    # Act: Run the calculation function
    stats = calculate_putting_stats(sample_clean_df)

    # Assert: Check the calculated statistics against expected values

    # --- Average Putts and 3-Putt Avoidance ---
    # Putts are [1, 1, 2, 2, 1, 3]. Avg = 1.67. 5/6 holes are <= 2 putts.
    assert stats["avg_putts_per_hole"] == pytest.approx(1.67, 0.01)
    assert stats["three_putt_avoidance_pct"] == pytest.approx(83.33, 0.01)

    # --- Putt Distribution ---
    # 3x 1-putt, 2x 2-putts, 1x 3-putt
    assert stats["1_putt_pct"] == 50.0
    assert stats["2_putt_pct"] == pytest.approx(33.33, 0.01)
    assert stats["3_plus_putt_pct"] == pytest.approx(16.67, 0.01)

    # --- Average Putts per GIR vs Missed GIR ---
    # GIR putts: [1, 2, 1]. Avg = 1.33
    # Missed GIR putts: [1, 2, 3]. Avg = 2.0
    assert stats["avg_putts_per_gir"] == pytest.approx(1.33, 0.01)
    assert stats["avg_putts_per_missed_gir"] == 2.0

    # --- Handicap Average Putts per GIR vs Missed GIR ---
    # Handicap GIR putts (5 holes): [1, 1, 2, 1, 3]. Avg = 1.6
    # Missed Handicap GIR putts (1 hole): [2]. Avg = 2.0
    assert stats["avg_putts_per_handicap_gir"] == 1.6
    assert stats["avg_putts_per_missed_handicap_gir"] == 2.0
