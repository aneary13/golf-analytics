import pytest
from src.visualisations import (
    create_scoring_bar_chart,
    create_score_distribution_chart,
    create_driving_dispersion_chart,
    create_approach_dispersion_chart,
    create_putt_distribution_chart
)

@pytest.fixture
def sample_stats_dict():
    """
    Provides a sample dictionary of calculated stats for testing visualization functions.
    """
    return {
        # Scoring Stats
        'avg_strokes_par_3': 3.5,
        'avg_strokes_par_4': 4.8,
        'avg_strokes_par_5': 5.9,
        'par_4_par_or_better_pct': 20.0,
        'par_4_bogey_pct': 50.0,
        'par_4_double_bogey_plus_pct': 30.0,
        'par_4_2_plus_points_pct': 60.0,
        'par_4_1_point_pct': 30.0,
        'par_4_0_points_pct': 10.0,
        # Driving Stats
        'dispersion': {'Fairway': 50.0, 'Left': 30.0, 'Right': 20.0},
        # Approach Stats
        'approach_dispersion': {'Green': 60.0, 'Short': 25.0, 'Left': 15.0},
        # Putting Stats
        '1_putt_pct': 30.0,
        '2_putt_pct': 60.0,
        '3_plus_putt_pct': 10.0,
    }

def test_create_scoring_bar_chart(sample_stats_dict):
    """
    Tests that the scoring bar chart is created with the correct data and layout.
    """
    fig = create_scoring_bar_chart(sample_stats_dict)
    assert fig.layout.title.text == 'Average Strokes by Par Type'
    trace = fig.data[0]
    assert trace.type == 'bar'
    assert list(trace.x) == ['Par 3', 'Par 4', 'Par 5']
    assert list(trace.y) == [3.5, 4.8, 5.9]

def test_create_score_distribution_chart_vs_par(sample_stats_dict):
    """
    Tests the score distribution donut chart (vs Par) is created correctly.
    """
    fig = create_score_distribution_chart(sample_stats_dict, par_type=4, by_points=False)
    assert 'vs Par' in fig.layout.title.text
    trace = fig.data[0]
    assert trace.type == 'pie'
    assert list(trace.labels) == ['Par or Better', 'Bogey', 'Double Bogey+']
    assert list(trace.values) == [20.0, 50.0, 30.0]
    assert trace.hole == 0.4

def test_create_score_distribution_chart_by_points(sample_stats_dict):
    """
    Tests the score distribution donut chart (by Points) is created correctly.
    """
    fig = create_score_distribution_chart(sample_stats_dict, par_type=4, by_points=True)
    assert 'Points' in fig.layout.title.text
    trace = fig.data[0]
    assert list(trace.labels) == ['2+ Points', '1 Point', '0 Points']
    assert list(trace.values) == [60.0, 30.0, 10.0]

def test_create_driving_dispersion_chart(sample_stats_dict):
    """
    Tests that the driving dispersion pie chart is created correctly.
    """
    fig = create_driving_dispersion_chart(sample_stats_dict)
    assert fig.layout.title.text == 'Tee Shot Dispersion'
    trace = fig.data[0]
    assert trace.type == 'pie'
    assert set(trace.labels) == {'Fairway', 'Left', 'Right'}
    assert set(trace.values) == {50.0, 30.0, 20.0}

def test_create_approach_dispersion_chart(sample_stats_dict):
    """
    Tests that the approach dispersion pie chart is created correctly.
    """
    fig = create_approach_dispersion_chart(sample_stats_dict)
    assert fig.layout.title.text == 'Approach Shot Dispersion'
    trace = fig.data[0]
    assert trace.type == 'pie'
    assert set(trace.labels) == {'Green', 'Short', 'Left'}
    assert set(trace.values) == {60.0, 25.0, 15.0}

def test_create_putt_distribution_chart(sample_stats_dict):
    """
    Tests that the putt distribution donut chart is created correctly.
    """
    fig = create_putt_distribution_chart(sample_stats_dict)
    assert fig.layout.title.text == 'Putt Distribution per Hole'
    trace = fig.data[0]
    assert trace.type == 'pie'
    assert list(trace.labels) == ['1-Putt', '2-Putts', '3+ Putts']
    assert list(trace.values) == [30.0, 60.0, 10.0]
    assert trace.hole == 0.4
