import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="wide")

# Load transactions
def load_transactions():
    with open('transactions.json', 'r') as f:
        return pd.DataFrame(json.load(f))

# Sidebar for adding new transactions
st.sidebar.title("Add Transaction")
description = st.sidebar.text_input("Description")
amount = st.sidebar.number_input("Amount", min_value=0.0, step=0.01)
type = st.sidebar.selectbox("Type", ["Income", "Expense"])
date = st.sidebar.date_input("Date", value=datetime.now().date())  # New date field

if st.sidebar.button("Add Transaction"):
    if description and amount:
        new_transaction = {
            "description": description,
            "amount": amount,
            "type": type,
            "date": date.strftime('%Y-%m-%d')  # Save date in 'YYYY-MM-DD' format
        }
        with open('transactions.json', 'r') as f:
            transactions = json.load(f)
        transactions.insert(0, new_transaction)  # Insert at the beginning for reverse order display
        with open('transactions.json', 'w') as f:
            json.dump(transactions, f, indent=4)
        st.sidebar.success("Transaction added successfully!")

# Load transactions data
df = load_transactions()
df['date'] = pd.to_datetime(df['date'])  # Convert date field to datetime
df = df.sort_values(by='date', ascending=False).reset_index(drop=True)  # Display newest transactions first

# Tab Layout
tab1, tab2 = st.tabs(["Transactions", "Analyze"])

# Tab 1: Transactions Table
with tab1:
    st.title("All Transactions")
    st.dataframe(df)

# Tab 2: Analysis
with tab2:
    st.title("Analyze Financial Data")

    # Income vs Expense Pie Chart
    st.subheader("Income vs Expense")
    income_expense_data = df.groupby("type")["amount"].sum().reset_index()
    pie_chart = px.pie(income_expense_data, names="type", values="amount", title="Income vs Expense")
    st.plotly_chart(pie_chart)

    # Monthly Expense Line Chart
    st.subheader("Monthly Expenses")
    monthly_data = df[df['type'] == 'Expense'].resample('M', on='date')['amount'].sum().reset_index()
    line_chart = px.line(monthly_data, x='date', y='amount', title='Monthly Expenses')
    st.plotly_chart(line_chart)

    # Category-wise Bar Chart
    st.subheader("Category-wise Spending")
    category_data = df.groupby("description")["amount"].sum().reset_index()
    bar_chart = px.bar(category_data, x="description", y="amount", title="Spending by Category")
    st.plotly_chart(bar_chart)
