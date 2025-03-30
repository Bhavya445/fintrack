from fastapi import FastAPI, Request
import pathway as pw
import json
from datetime import datetime

app = FastAPI()

# Load existing transactions
def load_transactions():
    with open('transactions.json', 'r') as f:
        return json.load(f)

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
