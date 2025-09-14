from typing import Any

import plotly.graph_objects as go

# --- Scoring Visualizations ---


def create_scoring_bar_chart(stats: dict[str, Any]) -> go.Figure:
    """
    Creates a bar chart showing the average strokes for Par 3s, 4s, and 5s.

    Args:
        stats (Dict[str, Any]): The dictionary of scoring statistics.

    Returns:
        go.Figure: A Plotly bar chart figure.
    """
    par_types = ["Par 3", "Par 4", "Par 5"]
    avg_strokes = [
        stats.get("avg_strokes_par_3", 0),
        stats.get("avg_strokes_par_4", 0),
        stats.get("avg_strokes_par_5", 0),
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=par_types,
                y=avg_strokes,
                text=[f"{s:.2f}" for s in avg_strokes],
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title_text="Average Strokes by Par Type",
        xaxis_title="Par Type",
        yaxis_title="Average Strokes",
        template="plotly_white",
    )
    return fig


def create_score_distribution_chart(
    stats: dict[str, Any], par_type: int, by_points: bool = False
) -> go.Figure:
    """
    Creates a donut chart showing the score distribution for a given par type.

    Args:
        stats (Dict[str, Any]): The dictionary of scoring statistics.
        par_type (int): The par type to create the chart for (3, 4, or 5).
        by_points (bool): If True, shows distribution by Stableford points.
                          Otherwise, shows by score vs par.

    Returns:
        go.Figure: A Plotly donut chart figure.
    """
    if by_points:
        labels = ["2+ Points", "1 Point", "0 Points"]
        values = [
            stats.get(f"par_{par_type}_2_plus_points_pct", 0),
            stats.get(f"par_{par_type}_1_point_pct", 0),
            stats.get(f"par_{par_type}_0_points_pct", 0),
        ]
        title = f"Score Distribution (Points) for Par {par_type}s"
        colors = ["#2ca02c", "#1f77b4", "#d62728"]  # Green, Blue, Red
    else:
        labels = ["Par or Better", "Bogey", "Double Bogey+"]
        values = [
            stats.get(f"par_{par_type}_par_or_better_pct", 0),
            stats.get(f"par_{par_type}_bogey_pct", 0),
            stats.get(f"par_{par_type}_double_bogey_plus_pct", 0),
        ]
        title = f"Score Distribution (vs Par) for Par {par_type}s"
        colors = ["#2ca02c", "#ff7f0e", "#d62728"]  # Green, Orange, Red

    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, hole=0.4, marker_colors=colors)]
    )
    fig.update_layout(
        title_text=title,
        annotations=[dict(text="Scores", x=0.5, y=0.5, font_size=20, showarrow=False)],
    )
    return fig


# --- Driving Visualizations ---


def create_driving_dispersion_chart(stats: dict[str, Any]) -> go.Figure:
    """
    Creates a graphic representing a fairway to show tee shot dispersion.

    Args:
        stats (Dict[str, Any]): The dictionary of driving statistics.

    Returns:
        go.Figure: A Plotly figure with shapes and annotations.
    """
    dispersion = stats.get("dispersion", {})

    # Define the zones and their properties
    zones = {
        "OB Left": {"shape": (0, 1, 1, 5), "color": "#FF9999", "pos": (0.5, 3)},
        "Left": {"shape": (1, 1, 2, 5), "color": "#6B8E23", "pos": (1.5, 3)},
        "Fairway": {"shape": (2, 1, 3, 5), "color": "#90EE90", "pos": (2.5, 3)},
        "Right": {"shape": (3, 1, 4, 5), "color": "#6B8E23", "pos": (3.5, 3)},
        "OB Right": {"shape": (4, 1, 5, 5), "color": "#FF9999", "pos": (4.5, 3)},
        "Short": {"shape": (1, 0, 4, 1), "color": "#F0E68C", "pos": (2.5, 0.5)},
    }

    fig = go.Figure()

    # Add shapes and annotations for each zone
    for name, properties in zones.items():
        x0, y0, x1, y1 = properties["shape"]
        pct = dispersion.get(name, 0)

        fig.add_shape(
            type="rect",
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1,
            line=dict(color="White"),
            fillcolor=properties["color"],
            layer="below",
        )

        text_color = "Black" if name == "Fairway" else "White"

        # Always format the percentage, even if it's zero
        display_text = f"{pct:.1f}%"

        fig.add_annotation(
            x=properties["pos"][0],
            y=properties["pos"][1],
            text=f"<b>{name}</b><br>{display_text}",
            showarrow=False,
            font=dict(color=text_color, size=16),
            align="center",
        )

    fig.update_layout(
        title_text="Tee Shot Dispersion",
        xaxis=dict(visible=False, range=[0, 5]),
        yaxis=dict(visible=False, range=[0, 5]),
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        height=400,
    )
    return fig


def create_distance_by_location_chart(stats: dict[str, Any]) -> go.Figure:
    """
    Creates a graphic representing a fairway to show average drive distance by location.

    Args:
        stats (Dict[str, Any]): The dictionary of driving statistics.

    Returns:
        go.Figure: A Plotly figure with shapes and annotations.
    """
    avg_distances = stats.get("avg_dist_by_location", {})

    # Define the zones and their properties (same as dispersion chart)
    zones = {
        "OB Left": {"shape": (0, 1, 1, 5), "color": "#FF9999", "pos": (0.5, 3)},
        "Left": {"shape": (1, 1, 2, 5), "color": "#6B8E23", "pos": (1.5, 3)},
        "Fairway": {"shape": (2, 1, 3, 5), "color": "#90EE90", "pos": (2.5, 3)},
        "Right": {"shape": (3, 1, 4, 5), "color": "#6B8E23", "pos": (3.5, 3)},
        "OB Right": {"shape": (4, 1, 5, 5), "color": "#FF9999", "pos": (4.5, 3)},
        "Short": {"shape": (1, 0, 4, 1), "color": "#F0E68C", "pos": (2.5, 0.5)},
    }

    fig = go.Figure()

    # Add shapes and annotations for each zone
    for name, properties in zones.items():
        x0, y0, x1, y1 = properties["shape"]
        dist = avg_distances.get(name, 0)

        fig.add_shape(
            type="rect",
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1,
            line=dict(color="White"),
            fillcolor=properties["color"],
            layer="below",
        )

        text_color = "Black" if name == "Fairway" else "White"

        # Determine the text to display
        if name in ["OB Left", "OB Right"] or dist == 0:
            display_text = "—"
        else:
            display_text = f"{dist:.0f} yds"

        fig.add_annotation(
            x=properties["pos"][0],
            y=properties["pos"][1],
            text=f"<b>{name}</b><br>{display_text}",
            showarrow=False,
            font=dict(color=text_color, size=16),
            align="center",
        )

    fig.update_layout(
        title_text="Average Distance by Location",
        xaxis=dict(visible=False, range=[0, 5]),
        yaxis=dict(visible=False, range=[0, 5]),
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        height=400,
    )
    return fig


# --- Approach Visualizations ---


def create_approach_dispersion_chart(stats: dict[str, Any]) -> go.Figure:
    """
    Creates a graphic representing a green to show approach shot dispersion.

    Args:
        stats (Dict[str, Any]): The dictionary of approach statistics.

    Returns:
        go.Figure: A Plotly figure with shapes and annotations.
    """
    dispersion = stats.get("approach_dispersion", {})

    fig = go.Figure()

    # Define colors
    green_color = "#A8C9A8"
    fringe_color = "#7CA57C"

    # Add shapes for green and fringe
    fig.add_shape(
        type="circle",
        x0=0,
        y0=0,
        x1=6,
        y1=6,
        line_color=fringe_color,
        fillcolor=fringe_color,
        layer="below",
    )
    fig.add_shape(
        type="circle",
        x0=1,
        y0=1,
        x1=5,
        y1=5,
        line_color=green_color,
        fillcolor=green_color,
        layer="below",
    )

    # Add flagstick
    fig.add_shape(
        type="line", x0=3, y0=3, x1=3, y1=4.1, line=dict(color="Black", width=1)
    )
    fig.add_trace(
        go.Scatter(
            x=[3.082],
            y=[4.14],
            mode="text",
            text="🚩",
            textfont=dict(color="red", size=25),
        )
    )

    # Define annotation positions and map to data keys
    annotations = {
        "Long": {"pos": (3, 5.5), "data_key": "Long"},
        "Short": {"pos": (3, 0.5), "data_key": "Short"},
        "Left": {"pos": (0.5, 3), "data_key": "Left"},
        "Right": {"pos": (5.5, 3), "data_key": "Right"},
        "Green": {"pos": (3, 2.5), "data_key": "Green"},
    }

    # Add annotations for each zone
    for name, properties in annotations.items():
        pct = dispersion.get(properties["data_key"], 0)
        text_color = "Black" if name == "Green" else "White"
        display_text = f"<b>{name}</b><br>{pct:.1f}%"

        fig.add_annotation(
            x=properties["pos"][0],
            y=properties["pos"][1],
            text=display_text,
            showarrow=False,
            font=dict(color=text_color, size=16),
            align="center",
        )

    fig.update_layout(
        title_text="Approach Shot Dispersion",
        xaxis=dict(visible=False, range=[-1, 7]),
        yaxis=dict(visible=False, range=[-1, 7]),
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        height=500,
        showlegend=False,
    )
    return fig


# --- Putting Visualizations ---


def create_putt_distribution_chart(stats: dict[str, Any]) -> go.Figure:
    """
    Creates a donut chart showing the distribution of putts per hole.

    Args:
        stats (Dict[str, Any]): The dictionary of putting statistics.

    Returns:
        go.Figure: A Plotly donut chart figure.
    """
    labels = ["1-Putt", "2-Putts", "3+ Putts"]
    values = [
        stats.get("1_putt_pct", 0),
        stats.get("2_putt_pct", 0),
        stats.get("3_plus_putt_pct", 0),
    ]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_layout(
        title_text="Putt Distribution per Hole",
        annotations=[dict(text="Putts", x=0.5, y=0.5, font_size=20, showarrow=False)],
    )
    return fig
