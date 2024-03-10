from transformers import pipeline

# Load pre-trained BERT-based question answering model
nlp = pipeline(
    "question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad"
)

# Sample data (replace with your own data)


# Function to handle user queries
def handle_query(user_query, data):
    # Process the user query using the pre-trained model
    result = nlp(question=user_query, context=data)
    print(result)
    # Return the answer to the user
    return result["answer"]
