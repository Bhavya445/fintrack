import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime
from langchain_rag_agent import analyze_transactions  # Make sure this is imported correctly

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
date = st.sidebar.date_input("Date", value=datetime.now().date())

if st.sidebar.button("Add Transaction"):
    if description and amount:
        new_transaction = {
            "description": description,
            "amount": amount,
            "type": type,
            "date": date.strftime('%Y-%m-%d')
        }
        with open('transactions.json', 'r') as f:
            transactions = json.load(f)
        transactions.insert(0, new_transaction)
        with open('transactions.json', 'w') as f:
            json.dump(transactions, f, indent=4)
        st.sidebar.success("Transaction added successfully!")

# Load transactions data
df = load_transactions()
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])
df = df.sort_values(by='date', ascending=False).reset_index(drop=True)

# Calculate Total Income, Total Expense, and Total Balance
total_income = df[df['type'] == 'Income']['amount'].sum()
total_expense = df[df['type'] == 'Expense']['amount'].sum()
total_balance = total_income - total_expense

st.markdown(f"## 💰 Total Balance: ₹{total_balance:,.2f}")
st.markdown(f"### 📈 Total Income: ₹{total_income:,.2f} | 📉 Total Expense: ₹{total_expense:,.2f}")

# Filter Options
st.sidebar.title("Filter Transactions")
filter_type = st.sidebar.selectbox("Filter by Type", ["All", "Income", "Expense"])
filter_start_date = st.sidebar.date_input("Start Date", value=df['date'].min().date())
filter_end_date = st.sidebar.date_input("End Date", value=df['date'].max().date())
filter_keyword = st.sidebar.text_input("Search by Description")

if filter_type != "All":
    df = df[df['type'] == filter_type]
df = df[(df['date'] >= pd.to_datetime(filter_start_date)) & (df['date'] <= pd.to_datetime(filter_end_date))]
if filter_keyword:
    df = df[df['description'].str.contains(filter_keyword, case=False, na=False)]

# Tab Layout
tab1, tab2, tab3 = st.tabs(["Transactions", "Analyze", "AI Analysis"])

# Tab 1: Transactions Table
with tab1:
    st.title("All Transactions")
    st.write(df.to_html(index=False), unsafe_allow_html=True)

    
    #st.dataframe(df.reset_index(drop=True))


# Tab 2: Analysis
with tab2:
    st.title("Analyze Financial Data")

    st.subheader("Income vs Expense")
    income_expense_data = df.groupby("type")["amount"].sum().reset_index()
    pie_chart = px.pie(income_expense_data, names="type", values="amount", title="Income vs Expense")
    st.plotly_chart(pie_chart)

    st.subheader("Monthly Expenses")
    monthly_data = df[df['type'] == 'Expense'].resample('M', on='date')['amount'].sum().reset_index()
    line_chart = px.line(monthly_data, x='date', y='amount', title='Monthly Expenses')
    st.plotly_chart(line_chart)

    st.subheader("Weekly Expenses")
    weekly_data = df[df['type'] == 'Expense'].resample('W', on='date')['amount'].sum().reset_index()
    weekly_chart = px.line(weekly_data, x='date', y='amount', title="Weekly Expenses")
    st.plotly_chart(weekly_chart)

    st.subheader("Category-wise Spending")
    category_data = df.groupby("description")["amount"].sum().reset_index()
    bar_chart = px.bar(category_data, x="description", y="amount", title="Spending by Category")
    st.plotly_chart(bar_chart)

# Tab 3: AI Analysis
with tab3:
    st.title("AI Analysis")

    st.write("Ask your own questions related to your finances and get AI-powered responses!")

    user_query = st.text_input("Enter your question:", placeholder="e.g., Can I afford to buy a laptop worth ₹50,000?")
    if st.button("Run AI Analysis"):
        try:
            transactions = json.loads(df.to_json(orient='records'))
            if user_query.strip():
                analysis = analyze_transactions(transactions, user_query)
                st.write("### AI Response:")
                st.write(analysis)
            else:
                st.warning("Please enter a question to ask the AI.")
        except Exception as e:
            st.error(f"Error during AI analysis: {str(e)}")
