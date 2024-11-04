import os
secret_key = os.urandom(24).hex()  # Generates a random 24-byte string and converts it to hex
print(secret_key)
