from datetime import datetime, timedelta
import ephem
import math
import random
import matplotlib.pyplot as plt

def calculate_solar_angles(datetime_local, latitude_deg, longitude_deg, elevation_m, timezone_str):
    # Initialize an observer with the given coordinates and elevation
    observer = ephem.Observer()
    observer.lat = math.radians(latitude_deg)  # Convert latitude to radians
    observer.lon = math.radians(longitude_deg)  # Convert longitude to radians
    observer.elevation = elevation_m  # Elevation in meters

    # Convert local datetime to UTC (not used directly in this example)
    observer.date = datetime_local

    # Compute solar position
    sun = ephem.Sun(observer)
    sun.compute(observer)

    # Get solar azimuth and altitude (in radians)
    solar_azimuth_rad = sun.az  # Azimuth (radians)
    solar_altitude_rad = sun.alt  # Altitude (radians)

    # Convert azimuth and altitude to degrees
    solar_azimuth_deg = math.degrees(solar_azimuth_rad)
    solar_altitude_deg = math.degrees(solar_altitude_rad)

    return solar_azimuth_deg, solar_altitude_deg

def average_solar_angles(latitude_deg, longitude_deg, elevation_m, timezone_str):
    # Iterate over every minute in a specific day (e.g., January 1st, 2024)
    start_datetime = datetime(2024, 1, 1, 0, 0, 0)
    end_datetime = datetime(2024, 12, 31, 23, 59, 0)
    datetime_local = start_datetime

    # Lists to store azimuth and altitude values for each minute
    azimuth_values = []
    altitude_values = []

    # Iterate over every minute in the day
    while datetime_local <= end_datetime:
        azimuth, altitude = calculate_solar_angles(datetime_local, latitude_deg, longitude_deg, elevation_m, timezone_str)
        azimuth_values.append(azimuth)
        altitude_values.append(altitude)
        datetime_local += timedelta(minutes=10)

    # Calculate average azimuth and altitude
    avg_azimuth = sum(azimuth_values) / len(azimuth_values)
    avg_altitude = sum(altitude_values) / len(altitude_values)

    return avg_azimuth, avg_altitude

numPoints = 10

# Generate 200 random latitude and longitude pairs
random.seed(0)  # For reproducibility
latitudes = [random.uniform(-90, 90) for _ in range(numPoints)]
longitudes = [random.uniform(-180, 180) for _ in range(numPoints)]

# Calculate average solar angles for each pair
timezone_str = 'UTC'  # You can change this to your desired timezone
average_altitudes = []
average_azimuths = []

min_alt = [0, 0]
max_alt = [0, 0]

for lat, lon in zip(latitudes, longitudes):
    print(latitudes.index(lat)/numPoints)
    avg_azimuth, avg_altitude = average_solar_angles(lat, lon, 0, timezone_str)
    if avg_altitude < min_alt[0]:
        min_alt[0] = avg_altitude
        min_alt[1] = lat
    if avg_altitude > max_alt[0]:
        max_alt[0] = avg_altitude
        max_alt[1] = lat
    average_azimuths.append(avg_azimuth)
    average_altitudes.append(avg_altitude)

# Create plots
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Latitude vs. Average Solar Altitude
axs[0, 0].scatter(latitudes, average_altitudes, alpha=0.6)
axs[0, 0].set_xlabel('Latitude')
axs[0, 0].set_ylabel('Average Solar Altitude')
axs[0, 0].set_title('Latitude vs. Average Solar Altitude')

# Longitude vs. Average Solar Altitude
axs[0, 1].scatter(longitudes, average_altitudes, alpha=0.6)
axs[0, 1].set_xlabel('Longitude')
axs[0, 1].set_ylabel('Average Solar Altitude')
axs[0, 1].set_title('Longitude vs. Average Solar Altitude')

# Latitude vs. Average Solar Azimuth
axs[1, 0].scatter(latitudes, average_azimuths, alpha=0.6)
axs[1, 0].set_xlabel('Latitude')
axs[1, 0].set_ylabel('Average Solar Azimuth')
axs[1, 0].set_title('Latitude vs. Average Solar Azimuth')

# Longitude vs. Average Solar Azimuth
axs[1, 1].scatter(longitudes, average_azimuths, alpha=0.6)
axs[1, 1].set_xlabel('Longitude')
axs[1, 1].set_ylabel('Average Solar Azimuth')
axs[1, 1].set_title('Longitude vs. Average Solar Azimuth')

plt.tight_layout()
plt.show()

print(f"{max_alt}")
print(f"{min_alt}")
a = 1
