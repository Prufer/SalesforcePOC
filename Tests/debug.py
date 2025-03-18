from dotenv import load_dotenv, find_dotenv
import os
# Specify the path to your custom environment file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'UATConfigs.env')  # Adjust this path as needed
load_dotenv(dotenv_path)  # Load environment variables from the UATConfigs.env file


users = {}  # Dictionary to store users
i = 1

while True:
    email = os.getenv(f"USER_{i}_EMAIL")
    password = os.getenv(f"USER_{i}_PASSWORD")
    role = os.getenv(f"USER_{i}_ROLE")

    if not email or not password or not role:
        print(f"🔹 Stopping at USER_{i} (no more users found)")
        break

    users[role.strip().lower()] = {
        "email": email.strip(),
        "password": password.strip(),
        "role": role.strip(),
    }

    print(f"✅ Loaded: {role.strip().lower()} -> {email}")
    i += 1

print("Final Loaded Users:", users)
