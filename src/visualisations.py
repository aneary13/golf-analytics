import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any

# --- Scoring Visualizations ---

def create_scoring_bar_chart(stats: Dict[str, Any]) -> go.Figure:
    """
    Creates a bar chart showing the average strokes for Par 3s, 4s, and 5s.

    Args:
        stats (Dict[str, Any]): The dictionary of scoring statistics.

    Returns:
        go.Figure: A Plotly bar chart figure.
    """
    par_types = ['Par 3', 'Par 4', 'Par 5']
    avg_strokes = [
        stats.get('avg_strokes_par_3', 0),
        stats.get('avg_strokes_par_4', 0),
        stats.get('avg_strokes_par_5', 0)
    ]

    fig = go.Figure(data=[go.Bar(x=par_types, y=avg_strokes, text=[f'{s:.2f}' for s in avg_strokes], textposition='auto')])
    
    fig.update_layout(
        title_text='Average Strokes by Par Type',
        xaxis_title='Par Type',
        yaxis_title='Average Strokes',
        template='plotly_white'
    )
    return fig

def create_score_distribution_chart(stats: Dict[str, Any], par_type: int, by_points: bool = False) -> go.Figure:
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
        labels = ['2+ Points', '1 Point', '0 Points']
        values = [
            stats.get(f'par_{par_type}_2_plus_points_pct', 0),
            stats.get(f'par_{par_type}_1_point_pct', 0),
            stats.get(f'par_{par_type}_0_points_pct', 0)
        ]
        title = f'Score Distribution (Points) for Par {par_type}s'
        colors = ['#2ca02c', '#1f77b4', '#d62728'] # Green, Blue, Red
    else:
        labels = ['Par or Better', 'Bogey', 'Double Bogey+']
        values = [
            stats.get(f'par_{par_type}_par_or_better_pct', 0),
            stats.get(f'par_{par_type}_bogey_pct', 0),
            stats.get(f'par_{par_type}_double_bogey_plus_pct', 0)
        ]
        title = f'Score Distribution (vs Par) for Par {par_type}s'
        colors = ['#2ca02c', '#ff7f0e', '#d62728'] # Green, Orange, Red

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker_colors=colors)])
    fig.update_layout(
        title_text=title,
        annotations=[dict(text='Scores', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    return fig

# --- Driving Visualizations ---

def create_driving_dispersion_chart(stats: Dict[str, Any]) -> go.Figure:
    """
    Creates a pie chart showing the dispersion of tee shots.

    Args:
        stats (Dict[str, Any]): The dictionary of driving statistics.

    Returns:
        go.Figure: A Plotly pie chart figure.
    """
    dispersion_stats = stats.get('dispersion', {})
    labels = list(dispersion_stats.keys())
    values = list(dispersion_stats.values())

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text='Tee Shot Dispersion')
    return fig

# --- Approach Visualizations ---

def create_approach_dispersion_chart(stats: Dict[str, Any]) -> go.Figure:
    """
    Creates a pie chart showing the dispersion of approach shots.

    Args:
        stats (Dict[str, Any]): The dictionary of approach statistics.

    Returns:
        go.Figure: A Plotly pie chart figure.
    """
    dispersion_stats = stats.get('approach_dispersion', {})
    labels = list(dispersion_stats.keys())
    values = list(dispersion_stats.values())

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text='Approach Shot Dispersion')
    return fig

# --- Putting Visualizations ---

def create_putt_distribution_chart(stats: Dict[str, Any]) -> go.Figure:
    """
    Creates a donut chart showing the distribution of putts per hole.

    Args:
        stats (Dict[str, Any]): The dictionary of putting statistics.

    Returns:
        go.Figure: A Plotly donut chart figure.
    """
    labels = ['1-Putt', '2-Putts', '3+ Putts']
    values = [
        stats.get('1_putt_pct', 0),
        stats.get('2_putt_pct', 0),
        stats.get('3_plus_putt_pct', 0)
    ]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
    fig.update_layout(
        title_text='Putt Distribution per Hole',
        annotations=[dict(text='Putts', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    return fig
