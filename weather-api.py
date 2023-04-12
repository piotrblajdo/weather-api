import pandas as pd
import requests
import argparse
import logging

API_COLUMNS = ["city", "temp", "wind"]
LOCATIONS = [
    "Copenhagen, Denmark",
    "Brussels, Belgium",
    "Lodz, Poland",
    "Islamabad, Pakistan",
]
SCOPE = 30


def parse_request(json_response):
    locations_weather = []

    city = json_response.get("address")
    days = json_response.get("days")
    for day in days:
        row_location_weather = [city, day.get("temp", 0), day.get("temp", 0)]
        locations_weather.append(row_location_weather)

    df_locations_weather = pd.DataFrame(locations_weather, columns=API_COLUMNS)

    df_result = pd.DataFrame([city], columns=["city"])
    for col in API_COLUMNS[1:]:
        df_result[f"{col}_avg"] = df_locations_weather["temp"].mean(axis=0)
        df_result[f"{col}_median"] = df_locations_weather["temp"].median(axis=0)

    return df_result


def process_locations():
    df_locations = pd.DataFrame()
    for location in LOCATIONS:
        try:
            url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/last{SCOPE}days?unitGroup=metric&key={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                df_location = parse_request(response.json())
                df_locations = df_locations.append(df_location)
            else:
                logging.error(response.text)
        except Exception as ex:
            logging.error(ex.text)

    return df_locations


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--api_key', type=str, help='required to get data from api', required=True)
    args = parser.parse_args()
    API_KEY = args.api_key

    result_locations = process_locations().reset_index(drop=True)
    if result_locations.empty:
        print("It gets the error during prepare result")
    else:
        print(result_locations)
