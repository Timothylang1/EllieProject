from twilio.rest import Client


client = Client(account_sid, auth_token)

message = client.messages.create(
        messaging_service_sid='MG9e2e885ec0b38bda169078f08b404001', # Replace with from_= originating phone number (preferably Ellie's)
        body="I'm watching you", # Message
        to='+16504474476' # Receiving phone number
)

print(message.status)
print(message.date_created)
print(message.price)
print(message.feedback)
print(message.error_message)
print(message.error_code)
print(message.date_sent)