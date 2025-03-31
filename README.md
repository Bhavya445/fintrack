# FinTrack: AI-Powered Transaction Analysis

FinTrack is a web application designed to track and analyze financial transactions using AI. It integrates a Fetch.ai agent with LangChain's RAG (Retrieval-Augmented Generation) capabilities to provide insights into transaction data.

## Features
- **Transaction Tracking:** Users can add, view, and filter transactions based on type, date, and description.
- **AI Analysis:** The application uses a Fetch.ai agent to analyze transactions and provide insights.
- **Data Visualization:** Includes interactive charts to visualize income vs expense, monthly expenses, and category-wise spending.

## Requirements
- Python 3.8 or higher (avoid Python 3.13 as it's experimental)
- FastAPI
- Streamlit
- LangChain
- Cohere API Key

## Setup
### Install Dependencies:
```bash
pip install fastapi uvicorn streamlit pandas plotly json langchain-cohere cohere
```

### Set Cohere API Key:
Set an environment variable for your Cohere API key:
```bash
export COHERE_API_KEY="your-api-key"
```

### Run Applications:

- **Start FastAPI server:**
```bash
uvicorn app:app --reload
```

- **Start Streamlit application:**
```bash
streamlit run streamlit_app.py
```

## Usage
### Add Transactions:
- Use the Streamlit interface to add new transactions.
- Select transaction type, enter amount, description, and date.

### View Transactions:
- View all transactions in the "Transactions" tab.
- Filter transactions by type, date, and description.

### Run AI Analysis:
- Click "Run AI Analysis" in the "AI Analysis" tab to generate insights.

### View Analysis Results:
- Analysis results will be displayed in the "AI Analysis" tab.

## Troubleshooting
- **Dependency Issues:** Ensure all dependencies are installed and up-to-date.
- **API Key Errors:** Verify that your Cohere API key is correctly set as an environment variable.
- **Python Version:** Use Python 3.8 or higher for compatibility.

