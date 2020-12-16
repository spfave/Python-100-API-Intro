import requests
import smtplib
import datetime as dt
import dateutil.parser as dp
import parameters as pr


# Constants
MY_LAT = 38.880470
MY_LNG = -77.301872
DELTA_LOC = 5


# Functions
def utc_to_local(utc_dt, timezone=None):
    return utc_dt.replace(tzinfo=dt.timezone.utc).astimezone(tz=timezone)


def time_json_to_dt(time_json):
    return dp.parse(time_json)


def location_iss():
    """ Return coordinate (lat, long) location of International Space Station """

    api_iss = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url=api_iss)
    response.raise_for_status()

    latitude = float(response.json()["iss_position"]["latitude"])
    longitude = float(response.json()["iss_position"]["longitude"])
    return (latitude, longitude)


def time_sunrise_sunset(latitude, longitude):
    """ Return sunrise and sunset time at specified coordinates (lat, long)
        Uses Sunset and Sunrise time API: https://sunrise-sunset.org/api
    """
    api_sunrise_sunset = "https://api.sunrise-sunset.org/json"
    parameters = {
        "lat": latitude,
        "lng": longitude,
        "formatted": 0,
    }
    response = requests.get(url=api_sunrise_sunset, params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise_utc = time_json_to_dt(data["results"]["sunrise"])
    sunset_utc = time_json_to_dt(data["results"]["sunset"])
    sunrise = utc_to_local(sunrise_utc)
    sunset = utc_to_local(sunset_utc)

    return (sunrise, sunset)


def send_iss_email():
    subject = "Look Up for the ISS!"
    message = "Quick, look up at the night sky the ISS is passing by"
    email_msg = f"Subject: {subject}\n\n\{message}"

    with smtplib.SMTP("smpt.gmail.com") as connection:
        connection.starttls()
        connection.login(user=pr.my_email, password=pr.password)
        connection.sendmail(
            from_addr=pr.my_email,
            to_addrs=pr.to_email,
            msg=email_msg
        )


# Main
(iss_lat, iss_lng) = location_iss()
(sunrise, sunset) = time_sunrise_sunset(MY_LAT, MY_LNG)
time_now = dt.datetime.now()


# Check ISS is close to my location
if abs(MY_LAT-iss_lat) < DELTA_LOC and abs(MY_LNG-iss_lng) < DELTA_LOC:
    # Check if it is currently night
    if time_now.time() < sunrise.time() or time_now.time() > sunset.time():
        # If both conditions are true send email to self to look up
        send_iss_email()
