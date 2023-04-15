import requests
import datetime

# Set the latitude and longitude coordinates for London, UTC
lat = 51.5074
lng = -0.1278

# Loop through each day in March 2023 and get the sunrise time for London, UTC
for day in range(1, 32):
    date = datetime.date(2023, 3, day)
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date}&formatted=0"
    response = requests.get(url)
    data = response.json()
    sunrise_time = data["results"]["sunrise"]
    print(f"Sunrise on {date}: {sunrise_time}")
