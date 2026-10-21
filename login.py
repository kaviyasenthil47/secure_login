
from database import Database
from auth import verify_password


def login_user(user_name, password):
    db = Database()

    try:
        user = db.get_user_by_username(user_name.strip())

        if user is None:
            return False, "Invalid username or password."

        if not verify_password(password, user["password_hash"]):
            return False, "Invalid username or password."

        return True, "Login successful."

    finally:
        db.close()


if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")

    success, message = login_user(username, password)
    print(message)
