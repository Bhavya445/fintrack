from langchain.llms import Cohere
from langchain import PromptTemplate, LLMChain

# Pass API key directly (if not using environment variables)
cohere_api_key = "6wRbzw1Hy8tSLfyPpbnXP6gNEMXq2EZ9Wgf2JIzv"

# Initialize Cohere model
cohere_model = Cohere(
    cohere_api_key=cohere_api_key,
    max_tokens=256,
    temperature=0.75
)

# Define a prompt template for transaction analysis with user queries
template = PromptTemplate(
    input_variables=["transactions", "user_query"],
    template="""
    You are a smart financial assistant. Here are some recent transactions:
    {transactions}
    
    The user asks: {user_query}
    Provide a helpful, accurate, and friendly response based on the transactions.
    Please keep in mind the currency is in INR.
    If the user asks about a specific transaction, provide details about it.
    If the user asks for general financial advice, provide that too.
    If the user asks for a summary, summarize the transactions.
    If the user asks for a specific analysis, provide that analysis.
    If the user asks about trends, provide insights based on the transactions.
    
    """
)

# Create a chain to generate analysis or respond to user queries
analysis_chain = LLMChain(
    llm=cohere_model,
    prompt=template,
)

# Function to analyze transactions or respond to user queries
def analyze_transactions(transactions, user_query):
    transaction_text = "\n".join([f"{t['description']}: {t['amount']}" for t in transactions])
    return analysis_chain.run({"transactions": transaction_text, "user_query": user_query})

# Example usage (for testing purposes)
if __name__ == "__main__":
    import json
    with open('transactions.json', 'r') as f:
        transactions = json.load(f)
    
    # User can ask their own questions
    user_query = input("What would you like to ask about your transactions? ")
    response = analyze_transactions(transactions, user_query)
    print(response)
