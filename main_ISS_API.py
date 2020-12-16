import requests
import datetime as dt
import dateutil.parser as dp


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


# Main
(iss_lat, iss_lng) = location_iss()
(sunrise, sunset) = time_sunrise_sunset(MY_LAT, MY_LNG)
time_now = dt.datetime.now()


# todo: check ISS is close to my location


# todo: check if it is currently dark
# todo: if both conditions ture send email to self to look up
