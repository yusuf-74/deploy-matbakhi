from twilio.rest import Client
from decouple import config

account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)


def send_message(to: str, message: str) -> None:
    _ = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=to
    )
