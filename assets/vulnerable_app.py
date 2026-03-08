import pickle
import os


def load_user_data(filename):
    """Load user data from pickle file."""
    with open(filename, 'rb') as f:
        return pickle.load(f)  # Vulnerable to arbitrary code execution


def execute_query(user_input):
    """Execute SQL query."""
    query = f"SELECT * FROM users WHERE name = '{user_input}'"  # SQL injection
    return db.execute(query)


def process_file(filepath):
    """Process uploaded file."""
    os.system(f"convert {filepath} output.jpg")  # Command injection


API_KEY = "sk-1234567890abcdef"  # Hardcoded secret
