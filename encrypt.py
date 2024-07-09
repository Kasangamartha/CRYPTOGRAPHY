from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def generate_key():
    return os.urandom(32)  # AES-256 key

def encrypt_message(message, key):
    iv = os.urandom(16)  # Initialization vector
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    
    return iv + encrypted_message  # Return IV + encrypted message

def decrypt_message(encrypted_message, key):
    iv = encrypted_message[:16]
    encrypted_message = encrypted_message[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    message = unpadder.update(padded_message) + unpadder.finalize()
    
    return message.decode()

# Example usage
message = "Hello, this is a secret message!"
key = generate_key()
print("Generated Key:", key)

encrypted_message = encrypt_message(message, key)
print("Encrypted Message:", encrypted_message)

decrypted_message = decrypt_message(encrypted_message, key)
print("Decrypted Message:", decrypted_message)