import requests
import datetime as dt


# Constants
MY_LAT = 38.880470
MY_LNG = -77.301872
DELTA_LOC = 5


# Functions
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=dt.timezone.utc).astimezone(tz=None)


def location_iss():
    """ Return coordinate (lat, long) location of International Space Station """

    api_iss = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url=api_iss)
    response.raise_for_status()

    latitude = response.json()["iss_position"]["latitude"]
    longitude = response.json()["iss_position"]["longitude"]
    coordinates = (latitude, longitude)
    return coordinates


print(location_iss())


# todo: sunset sunrise class
# parameters = {
#     "lat": MY_LAT,
#     "lng": MY_LNG,
#     "formatted": 0,
# }

# # Sunset and Sunrise time API: https://sunrise-sunset.org/api
# response = requests.get(
#     url="https://api.sunrise-sunset.org/json", params=parameters)
# response.raise_for_status()

# data = response.json()
# sunrise = data["results"]["sunrise"].split("T")[1].split(":")
# sunset = data["results"]["sunset"].split("T")[1].split(":")

# print(sunrise)
# print(sunset)

# time_now = dt.datetime.utcnow()
# print(time_now)


# todo: check ISS is close to my location
# todo: check if it is currently dark
# todo: if both conditions ture send email to self to look up
