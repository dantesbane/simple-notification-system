from twilio.rest import Client
from CONF import ACCOUNT_SID, AUTH_TOKEN, TWILIO_NUMBER, RECIPIENT_NUMBER

# in this part you have to replace account_sid
# auth_token, twilio_number, recipient_number with your actual credential



# Create Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)


def sendmessage(message,mobile_no):
    message = client.messages.create(
        body=message,
        from_=TWILIO_NUMBER,
        to=RECIPIENT_NUMBER
    )
    print(f"Message sent with SID: {message.sid}&quot;")


