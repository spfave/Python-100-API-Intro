import requests


# Main
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

latitude = response.json()["iss_position"]["latitude"]
longitude = response.json()["iss_position"]["longitude"]

coordinates = (latitude, longitude)
print(coordinates)