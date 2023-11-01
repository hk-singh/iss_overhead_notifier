import requests
from datetime import datetime
import smtplib
import time

MY_COORD = [51.752022, -1.257726]


# MY_COORD = [51.4511, 11.3750]

# function to check if the ISS is overhead
def is_iss_overhead():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()

    position = iss_response.json()["iss_position"]
    iss_latitude = float(position["latitude"])
    iss_longitude = float(position["longitude"])

    if MY_COORD[0] - 5 < iss_latitude < MY_COORD[0] + 5:
        if MY_COORD[1] - 5 < iss_longitude < MY_COORD[1] + 5:
            return True
    else:
        return False


# function to check if it is dark now
def is_it_dark():
    now = datetime.now()
    parameters = {
        "lat": MY_COORD[0],
        "lng": MY_COORD[1],
        "formatted": 0,
    }
    # sending the API request
    sun_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    sunrise = sun_response.json()["results"]["sunrise"]
    sunset = sun_response.json()["results"]["sunset"]
    sunrise_hour = int(sunrise.split("T")[1].split(":")[0])
    sunset_hour = int(sunset.split("T")[1].split(":")[0])
    # Checking if it is dark
    if sunset_hour < now.hour or now.hour < sunrise_hour:
        return True
    else:
        return False


# Checking if it is dark and if ISS is overhead
while True:
    time.sleep(60)
    if is_it_dark() and is_iss_overhead():
        print("Look up")
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up👆🏼\n\n The ISS is above you in the sky."
        )
    else:
        print("Better luck next time")
