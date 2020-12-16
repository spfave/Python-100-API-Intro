import requests
import datetime as dt
import dateutil.parser as dp


# Constants
MY_LAT = 38.880470
MY_LNG = -77.301872
DELTA_LOC = 5


# Functions
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=dt.timezone.utc).astimezone(tz=None)


def time_json_to_dt(time_json):
    return dp.parse(time_json)

    # time_format = "%Y-%m-%dT%H:%M:%S.%f"
    # return dt.datetime.strptime(time_json, time_format)


def location_iss():
    """ Return coordinate (lat, long) location of International Space Station """

    api_iss = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url=api_iss)
    response.raise_for_status()

    latitude = response.json()["iss_position"]["latitude"]
    longitude = response.json()["iss_position"]["longitude"]
    return (latitude, longitude)


# print(location_iss())


# todo: sunset sunrise class
def sunrise_sunset_time(latitude, longitude):
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
    sunrise = data["results"]["sunrise"]  # .split("T")[1].split(":")
    sunset = data["results"]["sunset"]  # .split("T")[1].split(":")
    print(sunrise, sunset)

    sunrise_dt = time_json_to_dt(data["results"]["sunrise"])
    sunset_dt = time_json_to_dt(data["results"]["sunset"])
    print(sunrise_dt, sunset_dt)
    return (sunrise, sunset)


print(sunrise_sunset_time(MY_LAT, MY_LNG))

# print(sunrise)
# print(sunset)

time_now = dt.datetime.now()
print(time_now)


# todo: check ISS is close to my location
# todo: check if it is currently dark
# todo: if both conditions ture send email to self to look up
