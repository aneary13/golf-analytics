import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.data_loader import load_data

# Define the path to the test data directory
TEST_DATA_DIR = Path(__file__).parent / "test_data"

# Create a sample DataFrame that mimics the structure of your Google Sheet
@pytest.fixture
def mock_gsheet_data():
    """
    Provides a representative sample DataFrame for testing by loading it
    from a dedicated CSV file.
    """
    # Load the mock data from the CSV file
    csv_path = TEST_DATA_DIR / "mock_data.csv"
    df = pd.read_csv(csv_path)
    return df

# Test the successful data loading and cleaning path
def test_load_data_success(mock_gsheet_data):
    """
    Tests that load_data successfully reads, cleans, and returns a DataFrame
    when the connection is successful.
    """
    # Use patch to replace the streamlit GSheetsConnection
    with patch('src.data_loader.st.connection') as mock_st_connection:
        # Arrange: Configure the mock to return our sample data from the fixture
        mock_conn = MagicMock()
        mock_conn.read.return_value = mock_gsheet_data.copy() # Use a copy to avoid side effects
        mock_st_connection.return_value = mock_conn

        # Act: Call the function we are testing
        result_df = load_data()

        # Assert: Check that the data was processed correctly
        assert not result_df.empty
        
        # --- Check Data Type Conversions ---
        # Check date conversion (assuming DD/MM/YYYY format)
        assert result_df['Date'].iloc[0] == pd.Timestamp('2025-08-05')
        
        # Check numeric conversion
        assert result_df['Par'].iloc[2] == 3
        assert result_df['Strokes'].iloc[2] == 3
        
        # --- Check 'Yes'/'No' to 1/0 Mapping ---
        # First row: FIR is 'Yes' -> should be 1.0
        assert result_df['FIR'].iloc[0] == 1.0
        # Third row: GIR is 'Yes' -> should be 1.0
        assert result_df['GIR'].iloc[2] == 1.0
        # Second row: GIR is 'No' -> should be 0.0
        assert result_df['GIR'].iloc[1] == 0.0


# Test the failure path
def test_load_data_failure():
    """
    Tests that load_data returns an empty DataFrame when the connection
    raises an exception.
    """
    # Arrange: Configure the mock to simulate a connection error
    with patch('src.data_loader.st.connection') as mock_st_connection:
        mock_st_connection.side_effect = Exception("Simulated connection error")

        # Act: Call the function
        result_df = load_data()

        # Assert: Check that an empty DataFrame is returned
        assert result_df.empty
