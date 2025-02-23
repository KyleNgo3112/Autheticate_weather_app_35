import requests
import os
from twilio.rest import Client

OWN_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key= os.environ.get("OWM_API_KEY")
# Twilio credentials
account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")

weather_params = {
    "lat" : -6.175110,
    "lon" : 106.865036,
    "appid" : api_key,
    "cnt" : 4,
    }

response = requests.get(OWN_Endpoint, params=weather_params)
response.raise_for_status()
# print(response.status_code) test if it is success
weather_data = response.json()
# print(weather_data["list"][0]["weather"][0]["id"])

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    # Send an SMS
    message = client.messages.create(
        body="It is going to rain today. Remember to bring an umbrella or coat what ever you prefer",
        from_='+myNum',  # Replace with your Twilio phone number
        to='+yourNum'      # Replace with the recipient's phone number
    )
    print(message.status)
    print(f"Message sent! SID: {message.sid}")