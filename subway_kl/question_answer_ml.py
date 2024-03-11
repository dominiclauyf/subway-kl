import logging

import tensorflow as tf
from transformers import pipeline

logging.getLogger("transformers").setLevel(logging.ERROR)
tf.get_logger().setLevel(logging.ERROR)

# Load pre-trained BERT-based question answering model
nlp = pipeline(
    "question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad"
)

# Sample data (replace with your own data)


# Function to handle user queries
def handle_query(user_query, datas):
    current_score = 0
    current_answer = ""
    for data in datas:
        if not data:
            continue

        result = nlp(question=user_query, context=data.rstrip())

        if result["score"] > 0.90:
            return result["score"], result["answer"]
        if result["score"] > current_score:
            current_score = result["score"]
            current_answer = result["answer"]
    # Return the answer to the user
    return current_score, current_answer
