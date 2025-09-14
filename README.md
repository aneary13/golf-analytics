# Golf Performance Analytics Dashboard ⛳️

This project is a Streamlit web application designed to analyze personal golf round data. It connects to a Google Sheet, calculates a comprehensive set of performance statistics, and visualizes them using interactive Plotly charts. The goal is to provide actionable insights into a golfer's game to help identify areas for improvement.

---

## 🚀 Live Application

The dashboard is deployed and publicly accessible via Streamlit Community Cloud.

**[Access the Live Dashboard Here](https://golf-analytics.streamlit.app)**

---

## Features

- **Live & Deployed:** Accessible from any device, including mobile.
- **Dashboard Interface:** Clean, tab-based layout built with Streamlit.
- **Dynamic Data:** Fetches the latest round data directly from a Google Sheet.
- **Interactive Filters:** Filter data by course, date range, and round selection (All, Recent, Best of).
- **Comprehensive Stats:** Calculates metrics for all major facets of the game: Scoring, Driving, Approach, Short Game, and Putting.
- **Interactive Visualizations:** Uses Plotly to create engaging custom graphics.
- **Automated Code Quality:** Uses Ruff for linting/formatting and pre-commit hooks to ensure code consistency.
- **CI/CD Pipeline:** Deploys automatically to Streamlit Cloud via a GitHub Actions CI pipeline that runs tests on every push.

---

## 🛠 Setup & Installation

This project uses [Poetry](https://python-poetry.org/) for dependency and environment management.

**Python Version:** This project is developed and tested with **Python 3.13** or higher.

### Step-by-Step Instructions

1. **Clone the repository:**

```bash
git clone <repository-url>
cd golf-analytics
```

1. **Install dependencies:**

This command creates a virtual environment and installs all packages from the `poetry.lock` file.

```bash
poetry install
```

1. **Set up Google API Credentials:**

- Follow the [Streamlit documentation](https://docs.streamlit.io/develop/tutorials/databases/private-gsheet) to get your Google service account credentials.
- Create a file at `.streamlit/secrets.toml` and add your credentials.

1. **Install Pre-Commit Hooks:**

This one-time setup command installs the hooks into your local Git repository.

```bash
poetry run pre-commit install
```

---

## Development

### Running the App Locally

To run the Streamlit application on your local machine:

```bash
poetry run streamlit run src/app.py
```

### Running Tests

To run the entire unit test suite using pytest:

```bash
poetry run pytest
```

### Formatting and Linting

This project uses **Ruff** for all formatting, linting, and import sorting. While the pre-commit hooks automate this process, you can also run the commands manually.

To format all files in the project:

```bash
poetry run ruff format .
```

To lint and automatically fix any issues found:

```bash
poetry run ruff check . --fix
```
