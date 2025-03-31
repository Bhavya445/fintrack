from fastapi import FastAPI, Request
import json
from datetime import datetime
from langchain_rag_agent import analyze_transactions  # Ensure this file is updated correctly

app = FastAPI()

# Load existing transactions
def load_transactions():
    try:
        with open('transactions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return an empty list if the file doesn't exist
        return []

# Save transactions
def save_transactions(transactions):
    with open('transactions.json', 'w') as f:
        json.dump(transactions, f, indent=4)

@app.post("/add_transaction/")
async def add_transaction(request: Request):
    data = await request.json()
    
    # Add current date if not provided
    if 'date' not in data or not data['date']:
        data['date'] = datetime.now().strftime('%Y-%m-%d')  # Saving date as 'YYYY-MM-DD'
    
    transactions = load_transactions()
    transactions.append(data)
    save_transactions(transactions)
    
    return {"message": "Transaction added successfully"}

@app.post("/analyze_transactions/")
async def analyze_transactions_endpoint():
    transactions = load_transactions()
    
    # Ensure transactions are loaded correctly before analysis
    if not transactions:
        return {"error": "No transactions available for analysis"}
    
    try:
        analysis = analyze_transactions(transactions)
        return {"analysis": analysis}
    except Exception as e:
        return {"error": str(e)}
