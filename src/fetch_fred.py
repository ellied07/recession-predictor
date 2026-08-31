import os

import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("FRED_API_KEY")

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_fred_series(series_id, start_date="1990-01-01"):
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": start_date,
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()["observations"]

    df = pd.DataFrame(data)

    df = df[["date", "value"]]

    df["date"] = pd.to_datetime(df["date"])

    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.rename(columns={"value": series_id})

    return df


if __name__ == "__main__":

    series = {
        "UNRATE": "unemployment_rate",
        "T10Y2Y": "yield_curve",
        "FEDFUNDS": "fed_funds_rate",
        "CPIAUCSL": "cpi",
        "INDPRO": "industrial_production",
        "HOUST": "housing_starts",
        "ICSA": "initial_claims",
        "UMCSENT": "consumer_sentiment",
        "USREC": "recession",
    }

    for series_id, name in series.items():
        print(f"Downloading {name}...")

        df = fetch_fred_series(series_id)

        df.to_csv(
            f"data/raw/{series_id}.csv",
            index=False
        )

    print("Done!")

