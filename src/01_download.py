from pathlib import Path

import pandas as pd

# 访问网站
import requests


COUNTRIES = [
    "DNK", "ITA", "PRT", "CHN", "KOR",
    "JPN", "SGP", "IND", "USA", "CAN",
    "GBR", "FRA", "DEU", "NLD", "SWE",
    "ESP", "AUS", "BRA", "MEX", "ZAF"
]

INDICATORS = {
    "IT.NET.USER.ZS": "internet_users_pct",
    "BX.GSR.CCIS.ZS": "ict_service_exports_pct",
    "SE.TER.ENRR": "tertiary_enrolment_pct",
    "NY.GDP.PCAP.CD": "gdp_per_capita_usd"
}

START_YEAR = 2015
END_YEAR = 2023


def download_indicator(code, name):

    countries = ";".join(COUNTRIES)

    url = (
        f"https://api.worldbank.org/v2/"
        f"country/{countries}/indicator/{code}"
    )

    params = {
        "format": "json",
        "per_page": 20000,
        "date": f"{START_YEAR}:{END_YEAR}"
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    #检查访问有没有失败
    response.raise_for_status()
    #把 JSON 转成 Python
    payload = response.json()

    if len(payload) < 2 or payload[1] is None:
        raise RuntimeError(
            f"No data returned for {code}"
        )

    rows = []

    for obs in payload[1]:

        rows.append({
            "country_code": obs["countryiso3code"],
            "country": obs["country"]["value"],
            "year": int(obs["date"]),
            "indicator_code": code,
            "indicator_name": name,
            "value": obs["value"]
        })

    return pd.DataFrame(rows)


all_data = []
#.items()是每次同时拿出 dictionary 的 key 和 value。
for code, name in INDICATORS.items():

    print(f"Downloading {name}...")

    df = download_indicator(
        code,
        name
    )

    all_data.append(df)

#concat是合并
raw = pd.concat(
    all_data,
    ignore_index=True
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

output = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "world_bank_raw.csv"
)

output.parent.mkdir(
    parents=True,
    exist_ok=True
)

raw.to_csv(
    output,
    index=False
)

print()
print("Download complete.")
print(f"Rows: {len(raw)}")
print(f"Countries: {raw['country_code'].nunique()}")
print(f"Saved to: {output}")