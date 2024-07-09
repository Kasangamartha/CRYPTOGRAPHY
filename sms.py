from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Check if environment variables are loaded
print("TWILIO_ACCOUNT_SID:", os.getenv('TWILIO_ACCOUNT_SID'))
print("TWILIO_AUTH_TOKEN:", os.getenv('TWILIO_AUTH_TOKEN'))
print("TWILIO_FROM_NUMBER:", os.getenv('TWILIO_FROM_NUMBER'))

def send_sms(to_number, message):
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_FROM_NUMBER')

        if not account_sid or not auth_token or not from_number:
            raise ValueError("One or more environment variables are missing.")

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )

        return message.sid
    except Exception as e:
        # Print detailed error message
        print(f"An error occurred: {e}")
        return None

# Sample usage
to_number = '+254720709484'  # Replace with the recipient's phone number in the correct format
message = 'Good evening Martha.'

message_sid = send_sms(to_number, message)
print("Message SID:", message_sid)