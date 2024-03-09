from transformers import pipeline

# Load pre-trained BERT-based question answering model
nlp = pipeline(
    "question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad"
)

# Sample data (replace with your own data)
outlets_data = {
    "outlets": [
        {"name": "Outlet A", "closing_time": "8:00 PM", "location": "Bangsar"},
        {"name": "Outlet B", "closing_time": "9:30 PM", "location": "KLCC"},
        {"name": "Outlet C", "closing_time": "10:00 PM", "location": "Bangsar"},
        # Add more outlet data as needed
    ]
}


# Function to handle user queries
def handle_query(user_query):
    # Process the user query using the pre-trained model
    result = nlp(question=user_query, context=outlets_data)

    # Return the answer to the user
    return result["answer"]


# Example queries
query1 = "Which are the outlets that close the latest?"
query2 = "How many outlets are located in Bangsar?"

# Process and print the results
result1 = handle_query(query1)
result2 = handle_query(query2)

print(f"Query 1: {result1}")
print(f"Query 2: {result2}")
