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
    Creates a graphic representing a fairway to show tee shot dispersion.

    Args:
        stats (Dict[str, Any]): The dictionary of driving statistics.

    Returns:
        go.Figure: A Plotly figure with shapes and annotations.
    """
    dispersion = stats.get('dispersion', {})
    
    # Define the zones and their properties
    zones = {
        'OB Left': {'shape': (0, 1, 1, 5), 'color': '#FF9999', 'pos': (0.5, 3)},
        'Left':    {'shape': (1, 1, 2, 5), 'color': '#6B8E23', 'pos': (1.5, 3)},
        'Fairway': {'shape': (2, 1, 3, 5), 'color': '#90EE90', 'pos': (2.5, 3)},
        'Right':   {'shape': (3, 1, 4, 5), 'color': '#6B8E23', 'pos': (3.5, 3)},
        'OB Right':{'shape': (4, 1, 5, 5), 'color': '#FF9999', 'pos': (4.5, 3)},
        'Short':   {'shape': (1, 0, 4, 1), 'color': '#F0E68C', 'pos': (2.5, 0.5)},
    }

    fig = go.Figure()

    # Add shapes and annotations for each zone
    for name, properties in zones.items():
        x0, y0, x1, y1 = properties['shape']
        pct = dispersion.get(name, 0)
        
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color="White"), fillcolor=properties['color'], layer='below')
        
        # Use a different text color for the light green fairway block
        text_color = "Black" if name == "Fairway" else "White"
        
        fig.add_annotation(x=properties['pos'][0], y=properties['pos'][1],
                           text=f"<b>{name}</b><br><span style='font-size: 20px;'>{pct:.1f}%</span>",
                           showarrow=False, font=dict(color=text_color, size=14), align="center")

    fig.update_layout(
        title_text='Tee Shot Dispersion',
        xaxis=dict(visible=False, range=[0, 5]),
        yaxis=dict(visible=False, range=[0, 5]),
        template='plotly_white',
        margin=dict(l=20, r=20, t=50, b=20),
        height=400
    )
    return fig

def create_distance_by_location_chart(stats: Dict[str, Any]) -> go.Figure:
    """
    Creates a graphic representing a fairway to show average tee shot distance by location.

    Args:
        stats (Dict[str, Any]): The dictionary of driving statistics.

    Returns:
        go.Figure: A Plotly figure with shapes and annotations.
    """
    avg_distances = stats.get('avg_dist_by_location', {})
    
    # Define the zones and their properties (same as dispersion chart)
    zones = {
        'OB Left': {'shape': (0, 1, 1, 5), 'color': '#FF9999', 'pos': (0.5, 3)},
        'Left':    {'shape': (1, 1, 2, 5), 'color': '#6B8E23', 'pos': (1.5, 3)},
        'Fairway': {'shape': (2, 1, 3, 5), 'color': '#90EE90', 'pos': (2.5, 3)},
        'Right':   {'shape': (3, 1, 4, 5), 'color': '#6B8E23', 'pos': (3.5, 3)},
        'OB Right':{'shape': (4, 1, 5, 5), 'color': '#FF9999', 'pos': (4.5, 3)},
        'Short':   {'shape': (1, 0, 4, 1), 'color': '#F0E68C', 'pos': (2.5, 0.5)},
    }

    fig = go.Figure()

    # Add shapes and annotations for each zone
    for name, properties in zones.items():
        x0, y0, x1, y1 = properties['shape']
        dist = avg_distances.get(name, 0)
        
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color="White"), fillcolor=properties['color'], layer='below')
        
        text_color = "Black" if name == "Fairway" else "White"
        
        fig.add_annotation(x=properties['pos'][0], y=properties['pos'][1],
                           text=f"<b>{name}</b><br><span style='font-size: 20px;'>{dist:.0f} yds</span>",
                           showarrow=False, font=dict(color=text_color, size=14), align="center")

    fig.update_layout(
        title_text='Average Distance by Location',
        xaxis=dict(visible=False, range=[0, 5]),
        yaxis=dict(visible=False, range=[0, 5]),
        template='plotly_white',
        margin=dict(l=20, r=20, t=50, b=20),
        height=400
    )
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
