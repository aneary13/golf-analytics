from typing import Any

import pandas as pd


def calculate_scoring_stats(df: pd.DataFrame) -> dict[str, Any]:
    """
    Calculates all scoring-related statistics from the provided DataFrame.

    Args:
        df (pd.DataFrame): The cleaned golf data.

    Returns:
        Dict[str, Any]: A dictionary containing all scoring statistics.
    """
    if df.empty:
        return {}

    stats = {}

    # --- 1. Average Strokes and Points ---
    # Group by Par to calculate average strokes for each par type
    avg_strokes_by_par = df.groupby("Par")["Strokes"].mean().round(2)
    stats["avg_strokes_par_3"] = avg_strokes_by_par.get(3, 0)
    stats["avg_strokes_par_4"] = avg_strokes_by_par.get(4, 0)
    stats["avg_strokes_par_5"] = avg_strokes_by_par.get(5, 0)

    # Calculate overall average Stableford points
    stats["avg_stableford_points"] = df["Score"].mean().round(2)

    # --- 2. Score Distribution (Strokes) ---
    # Calculate score relative to par
    df["Score vs Par"] = df["Strokes"] - df["Par"]

    for par_type in [3, 4, 5]:
        par_df = df[df["Par"] == par_type]
        if not par_df.empty:
            total_holes = len(par_df)
            stats[f"par_{par_type}_par_or_better_pct"] = (
                (par_df["Score vs Par"] <= 0).sum() / total_holes * 100
            )
            stats[f"par_{par_type}_bogey_pct"] = (
                (par_df["Score vs Par"] == 1).sum() / total_holes * 100
            )
            stats[f"par_{par_type}_double_bogey_plus_pct"] = (
                (par_df["Score vs Par"] >= 2).sum() / total_holes * 100
            )

    # --- 3. Score Distribution (Stableford) ---
    for par_type in [3, 4, 5]:
        par_df = df[df["Par"] == par_type]
        if not par_df.empty:
            total_holes = len(par_df)
            stats[f"par_{par_type}_2_plus_points_pct"] = (
                (par_df["Score"] >= 2).sum() / total_holes * 100
            )
            stats[f"par_{par_type}_1_point_pct"] = (
                (par_df["Score"] == 1).sum() / total_holes * 100
            )
            stats[f"par_{par_type}_0_points_pct"] = (
                (par_df["Score"] == 0).sum() / total_holes * 100
            )

    return stats


def calculate_driving_stats(df: pd.DataFrame) -> dict[str, Any]:
    """
    Calculates all driving-related statistics from the provided DataFrame.

    Args:
        df (pd.DataFrame): The cleaned golf data.

    Returns:
        Dict[str, Any]: A dictionary containing all driving statistics.
    """
    # Filter for holes where a tee shot is relevant (Par 4s and 5s)
    drive_df = df[df["Par"].isin([4, 5])].copy()
    if drive_df.empty:
        return {}

    stats = {}
    total_drives = len(drive_df)

    # --- FIR % and Ball in Play Rate ---
    stats["fir_pct"] = (drive_df["FIR"] == 1).sum() / total_drives * 100
    # Check if the location string starts with 'OB', handling potential NaN values
    stats["ball_in_play_rate_pct"] = (
        (~drive_df["Tee Shot Location"].str.startswith("OB", na=False)).sum()
        / total_drives
        * 100
    )

    # --- Tee Shot Dispersion ---
    location_counts = drive_df["Tee Shot Location"].value_counts(normalize=True) * 100
    stats["dispersion"] = location_counts.to_dict()

    # --- Tee Shot Distance ---
    stats["avg_drive_distance"] = drive_df["Tee Shot Distance"].mean()

    # Avg distance by location
    avg_dist_by_loc = drive_df.groupby("Tee Shot Location")["Tee Shot Distance"].mean()
    stats["avg_dist_by_location"] = avg_dist_by_loc.to_dict()

    # --- Breakdown by Par 4 vs Par 5 ---
    for par_type in [4, 5]:
        par_df = drive_df[drive_df["Par"] == par_type]
        if not par_df.empty:
            par_stats = {}
            total_par_drives = len(par_df)
            par_stats["fir_pct"] = (par_df["FIR"] == 1).sum() / total_par_drives * 100
            par_stats["ball_in_play_rate_pct"] = (
                (~par_df["Tee Shot Location"].str.startswith("OB", na=False)).sum()
                / total_par_drives
                * 100
            )
            par_stats["avg_distance"] = par_df["Tee Shot Distance"].mean()
            stats[f"par_{par_type}_driving"] = par_stats

    return stats


def calculate_approach_stats(df: pd.DataFrame) -> dict[str, Any]:
    """
    Calculates all approach-related statistics from the provided DataFrame.

    Args:
        df (pd.DataFrame): The cleaned golf data.

    Returns:
        Dict[str, Any]: A dictionary containing all approach statistics.
    """
    if df.empty:
        return {}

    stats = {}
    total_holes = len(df)

    # --- GIR % ---
    stats["gir_pct"] = df["GIR"].mean() * 100

    # --- Handicap GIR % ---
    # A Handicap GIR is when strokes to the green <= (Par - 2 + Handicap Shots)
    strokes_to_green = df["Strokes"] - df["Putts"]
    regulation_target = df["Par"] - 2 + df["Shots"]
    handicap_gir = (strokes_to_green <= regulation_target).sum()
    stats["handicap_gir_pct"] = (handicap_gir / total_holes) * 100

    # --- Approach Shot Dispersion ---
    location_counts = df["Approach Location"].value_counts(normalize=True) * 100
    stats["approach_dispersion"] = location_counts.to_dict()

    return stats


def calculate_short_game_stats(df: pd.DataFrame) -> dict[str, Any]:
    """
    Calculates all short game-related statistics from the provided DataFrame.

    Args:
        df (pd.DataFrame): The cleaned golf data.

    Returns:
        Dict[str, Any]: A dictionary containing all short game statistics.
    """
    if df.empty:
        return {}

    stats = {}

    # --- Average Strokes to Green from < 100y ---
    inside_100_df = df[df["Shots Inside 100y"] > 0]
    if not inside_100_df.empty:
        stats["avg_strokes_to_green_inside_100y"] = inside_100_df[
            "Shots Inside 100y"
        ].mean()

    # --- Scrambling % ---
    missed_gir_df = df[df["GIR"] == 0]
    if not missed_gir_df.empty:
        scrambled = (missed_gir_df["Strokes"] <= missed_gir_df["Par"]).sum()
        stats["scrambling_pct"] = (scrambled / len(missed_gir_df)) * 100

    # --- Handicap Scrambling % ---
    strokes_to_green = df["Strokes"] - df["Putts"]
    regulation_target = df["Par"] - 2 + df["Shots"]
    missed_handicap_gir_df = df[strokes_to_green > regulation_target]

    if not missed_handicap_gir_df.empty:
        net_par_or_better = (
            missed_handicap_gir_df["Strokes"] - missed_handicap_gir_df["Shots"]
            <= missed_handicap_gir_df["Par"]
        ).sum()
        stats["handicap_scrambling_pct"] = (
            net_par_or_better / len(missed_handicap_gir_df)
        ) * 100

    # --- Short Game Score ---
    if not inside_100_df.empty:
        short_game_score = inside_100_df["Shots Inside 100y"] + inside_100_df["Putts"]
        stats["short_game_score"] = short_game_score.mean()

    return stats


def calculate_putting_stats(df: pd.DataFrame) -> dict[str, Any]:
    """
    Calculates all putting-related statistics from the provided DataFrame.

    Args:
        df (pd.DataFrame): The cleaned golf data.

    Returns:
        Dict[str, Any]: A dictionary containing all putting statistics.
    """
    if df.empty or "Putts" not in df.columns:
        return {}

    stats = {}
    total_holes = len(df)

    # --- Average Putts and 3-Putt Avoidance ---
    stats["avg_putts_per_hole"] = df["Putts"].mean()
    stats["three_putt_avoidance_pct"] = (df["Putts"] <= 2).sum() / total_holes * 100

    # --- Putt Distribution ---
    putt_counts = df["Putts"].value_counts()
    stats["1_putt_pct"] = putt_counts.get(1, 0) / total_holes * 100
    stats["2_putt_pct"] = putt_counts.get(2, 0) / total_holes * 100
    stats["3_plus_putt_pct"] = (df["Putts"] >= 3).sum() / total_holes * 100

    # --- Average Putts per GIR vs Missed GIR ---
    gir_df = df[df["GIR"] == 1]
    missed_gir_df = df[df["GIR"] == 0]
    if not gir_df.empty:
        stats["avg_putts_per_gir"] = gir_df["Putts"].mean()
    if not missed_gir_df.empty:
        stats["avg_putts_per_missed_gir"] = missed_gir_df["Putts"].mean()

    # --- Handicap Average Putts per GIR vs Missed GIR ---
    strokes_to_green = df["Strokes"] - df["Putts"]
    regulation_target = df["Par"] - 2 + df["Shots"]
    df["is_handicap_gir"] = strokes_to_green <= regulation_target

    handicap_gir_df = df[df["is_handicap_gir"]]
    missed_handicap_gir_df = df[~df["is_handicap_gir"]]

    if not handicap_gir_df.empty:
        stats["avg_putts_per_handicap_gir"] = handicap_gir_df["Putts"].mean()
    if not missed_handicap_gir_df.empty:
        stats["avg_putts_per_missed_handicap_gir"] = missed_handicap_gir_df[
            "Putts"
        ].mean()

    return stats
