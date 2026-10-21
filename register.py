
import re
import bcrypt
from database import Database


def register_user(user_name, password):
    # 1. Validate inputs
    if not user_name or not password:
        return "Username and password are required."

    user_name = user_name.strip()

    if not re.fullmatch(r"[A-Za-z0-9_]{3,50}", user_name):
        return "Username must be 3-50 characters: letters, numbers or _."

    if len(password) < 8:
        return "Password must contain at least 8 characters."

    # 2. Hash the password
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # 3. Store the user
    db = Database()
    try:
        db.add_user((user_name, password_hash))
        return "Registration successful."
    except Exception as error:
        # MySQL duplicate-key error
        if getattr(error, "args", [None])[0] == 1062:
            return "Username already exists."
        raise
    finally:
        db.close()


if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")

    print(register_user(username, password))
