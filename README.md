# Golf Performance Analytics Dashboard ⛳️

This project is a Streamlit web application designed to analyze personal golf round data. It connects to a Google Sheet, calculates a comprehensive set of performance statistics, and visualizes them using interactive Plotly charts. The goal is to provide actionable insights into a golfer's game to help identify areas for improvement.

---

## 🚀 Live Application

The dashboard is deployed and publicly accessible via Streamlit Community Cloud.

**[Access the Live Dashboard Here](https://golf-analytics.streamlit.app)**

---

## ⛳️ Features

-   **Live & Deployed:** Accessible from any device, including mobile.
-   **Dashboard Interface:** Clean, tab-based layout built with Streamlit.
-   **Dynamic Data:** Fetches the latest round data directly from a Google Sheet.
-   **Interactive Filters:** Filter your data by course, date range or most recent rounds.
-   **Comprehensive Stats:** Calculates metrics for all major facets of the game: Scoring, Driving, Approach, Short Game, and Putting.
-   **Interactive Visualizations:** Uses Plotly to create engaging and filterable charts.
-   **Secure:** Manages Google API credentials securely using Streamlit's secrets management.

---

## 🛠 Setup & Installation

This project uses [Poetry](https://python-poetry.org/) for dependency and environment management.

**Python Version:** This project is developed and tested with **Python 3.13** or higher.

### Step-by-Step Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd golf_analytics
    ```

2.  **Install dependencies:**
    This command will create a virtual environment and install all necessary packages from the `poetry.lock` file (make sure you have **Poetry** installed on your machine).
    ```bash
    poetry install
    ```

3.  **Set up Google API Credentials:**
    -   Follow the [Streamlit documentation](https://docs.streamlit.io/develop/tutorials/databases/private-gsheet) to get your Google service account credentials.
    -   Create a file at `.streamlit/secrets.toml`.
    -   Add your credentials to the `secrets.toml` file in the correct format.

---

## ✅ Running Tests

This project uses `pytest` for unit testing. The tests are located in the `tests/` directory.

To run the entire test suite, execute:

```bash
poetry run pytest
```
