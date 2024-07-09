from flask import Flask, request, render_template, redirect, url_for
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from twilio.rest import Client
import re

app = Flask(__name__)

# AES 256 key generation
def generate_key():
    return os.urandom(32)

# Encryption function
def encrypt_message(message, key):
    iv = os.urandom(16)
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_message

# Decryption function
def decrypt_message(encrypted_message, key):
    iv = encrypted_message[:16]
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    try:
        padded_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        message = unpadder.update(padded_message) + unpadder.finalize()
        return message.decode()
    except Exception as e:
        raise ValueError(f"Decryption error: {str(e)}")

# Twilio configurations
account_sid = 'ACc7c4aecd00401d23f0cea539213daa16'
auth_token = '24600a1bf3e5a9b97a3b106d64192981'
twilio_client = Client(account_sid, auth_token)

def send_sms(body, to):
    if not re.match(r'^\+?[1-9]\d{1,14}$', to):
        raise ValueError("Invalid phone number format.")

    try:
        message = twilio_client.messages.create(
            body=body,
            from_='+16185912665',  # Your Twilio phone number
            to=to
        )
        return message.sid
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")
        return str(e)

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/encrypt')
def encrypt():
    return render_template('encryptmessage.html')

@app.route('/encrypted_message', methods=['POST'])
def sent_encrypted_message():
    phone_number = request.form['phone_number']
    message = request.form['message']
    key = generate_key()
    encrypted_message = encrypt_message(message, key)
    otp = key.hex()

    otp_message = f"Your OTP is: {otp}\nEncrypted message: {encrypted_message.hex()}"

    try:
        send_sms(otp_message, phone_number)
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Failed to send message: {str(e)}"

    return render_template('send.html')

@app.route('/decrypt')
def decrypt():
    return render_template('decryptmessage.html')

@app.route('/decrypted_message', methods=['POST'])
def decrypt_message_route():
    otp = request.form['otp']
    encrypted_message_hex = request.form['encrypted_message']
    key = bytes.fromhex(otp)
    encrypted_message = bytes.fromhex(encrypted_message_hex)
    
    try:
        decrypted_message = decrypt_message(encrypted_message, key)
        return render_template('decryptedmessage.html', decrypted_message=decrypted_message)
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return f"Decryption failed: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
