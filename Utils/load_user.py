import os
from dotenv import load_dotenv

def load_users():
    """Load all users from the .env file and return them as a dictionary with roles as keys."""
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'UATConfigs.env')
    load_dotenv(dotenv_path)  # Load environment variables from .env file

    users = {}
    i = 1
    while True:
        email = os.getenv(f"USER_{i}_EMAIL")
        password = os.getenv(f"USER_{i}_PASSWORD")
        role = os.getenv(f"USER_{i}_ROLE")

        if not email or not password or not role:
            break  # Stop if no more users are found

        # Use the role as the key
        users[role] = {
            "email": email,
            "password": password,
            "role": role
        }
        i += 1
    return users

# Load users once and store them globally
USERS = load_users()