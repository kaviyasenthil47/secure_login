
from auth import hash_password, verify_password

password = "Example@123"

hashed = hash_password(password)

print("Hashed password:", hashed)
print("Correct password:", verify_password(password, hashed))
print("Wrong password:", verify_password("Wrong@123", hashed))
