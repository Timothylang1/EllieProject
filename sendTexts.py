import twilio
# 3126103265


# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC1b6b8e92b7158f36445bbed7041b9f0e' # TWILIO SID
auth_token = '1d98bee4c5dc3406170bea3b4fe16cf4' # TWILIO AUTH TOKEN
client = Client(account_sid, auth_token)

message = client.messages.create(
    messaging_service_sid='MG9e2e885ec0b38bda169078f08b404001',
                              body="I'm watching you",
                              messaging_service_sid='MG9e2e885ec0b38bda169078f08b404001',
                              to='+16504474476'
                          )

print(message.status)
print(message.price)
print(message.feedback)
print(message.error_message)
print(message.error_code)
print(message.date_sent)