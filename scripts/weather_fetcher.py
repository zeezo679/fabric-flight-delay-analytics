import requests
import time
import csv
import os

# Replace with your actual airport list - export airports_to_query from Fabric first,
# e.g. as a small CSV: iata_code, latitude, longitude, min_date, max_date
airports = []  # load from your exported list
with open("untitled.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        airports.append({
            "iata_code": row["iata_code"],
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "min_date": row["min_date"],
            "max_date": row["max_date"]
        })

print(f"Loaded {len(airports)} airports")

output_file = "weather_results.csv"
already_done = set()

# Resume support: if the file already exists from a previous partial run, skip what's done
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        reader = csv.DictReader(f)
        already_done = {row["iata_code"] for row in reader}

write_header = not os.path.exists(output_file)

with open(output_file, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["iata_code", "date", "precipitation", "windspeed", "temp_max", "temp_min"])
    if write_header:
        writer.writeheader()

    for idx, row in enumerate(airports):
        if row["iata_code"] in already_done:
            continue

        try:
            resp = requests.get(
                "https://archive-api.open-meteo.com/v1/archive",
                params={
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "start_date": row["min_date"],
                    "end_date": row["max_date"],
                    "daily": "precipitation_sum,windspeed_10m_max,temperature_2m_max,temperature_2m_min",
                    "timezone": "UTC"
                },
                timeout=15
            )
            if resp.status_code == 200:
                data = resp.json()
                for i, d in enumerate(data["daily"]["time"]):
                    writer.writerow({
                        "iata_code": row["iata_code"],
                        "date": d,
                        "precipitation": data["daily"]["precipitation_sum"][i],
                        "windspeed": data["daily"]["windspeed_10m_max"][i],
                        "temp_max": data["daily"]["temperature_2m_max"][i],
                        "temp_min": data["daily"]["temperature_2m_min"][i],
                    })
                f.flush()  # write to disk immediately, don't wait for buffer
            else:
                print(f"Failed {row['iata_code']}: {resp.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error {row['iata_code']}: {e}")

        if idx % 20 == 0:
            print(f"{idx}/{len(airports)}")

        time.sleep(0.3)

print("Done.")