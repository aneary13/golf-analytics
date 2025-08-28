# Golf Performance Analytics Dashboard

This project is a Streamlit web application designed to analyse personal golf data. It connects to a Google Sheet, calculates a comprehensive set of performance statistics, and visualises them using interactive Plotly charts. The goal is to provide actionable insights into my golf game to help identify areas for improvement.


## ⛳️ Features

-   **Dashboard Interface:** Clean, tab-based layout built with Streamlit.
-   **Dynamic Data:** Fetches the latest round data directly from a Google Sheet.
-   **Comprehensive Stats:** Calculates metrics for all major facets of the game: Scoring, Driving, Approach, Short Game, and Putting.
-   **Interactive Visualizations:** Uses Plotly to create engaging and filterable charts.
-   **Secure:** Manages Google API credentials securely using Streamlit's secrets management.


## 🛠 Setup & Installation

This project uses [Poetry](https://python-poetry.org/) for dependency and environment management.

**Python Version:** This project is developed and tested with **Python 3.13** or higher.

### Step-by-Step Instructions

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd golf-analytics
    ```

2.  **Install dependencies:**
    This command will create a virtual environment and install all necessary packages from the `poetry.lock` file.
    ```bash
    poetry install
    ```

3.  **Set up Google API Credentials:**
    -   Follow the [Streamlit documentation](https://docs.streamlit.io/develop/tutorials/databases/private-gsheet) to get your Google service account credentials.
    -   Create a file at `.streamlit/secrets.toml`.
    -   Add your credentials to the `secrets.toml` file in the correct format. It should look something like this:
        ```toml
        # .streamlit/secrets.toml
        [gcp_service_account]
        type = "service_account"
        project_id = "your-google-project-id"
        private_key_id = "your-private-key-id"
        private_key = "-----BEGIN PRIVATE KEY-----\n..."
        client_email = "your-service-account-email@your-project.iam.gserviceaccount.com"
        client_id = "your-client-id"
        auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
        token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
        auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"
        client_x509_cert_url = "..."
        ```

## 🚀 Running the Application

To launch the Streamlit dashboard, run the following command from the root directory of the project:

```bash
poetry run streamlit run src/app.py
```


## ✅ Running Tests

This project uses pytest for unit testing. The tests are located in the tests/ directory.

To run the entire test suite, execute:

```bash
poetry run pytest
```