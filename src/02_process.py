from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "world_bank_raw.csv"
)

OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "country_year_indicators.csv"
)


df = pd.read_csv(INPUT)


# -------------------------
# Check duplicates
# -------------------------

key = [
    "country_code",
    "year",
    "indicator_name"
]

duplicates = df.duplicated(
    subset=key
).sum()

if duplicates > 0:
    raise ValueError(
        f"Found {duplicates} duplicate observations"
    )


# -------------------------
# Convert long → wide
# -------------------------

wide = df.pivot(
    index=[
        "country_code",
        "country",
        "year"
    ],
    columns="indicator_name",
    values="value"
).reset_index()

wide.columns.name = None


# -------------------------
# Create transformed GDP
# -------------------------

wide["log_gdp_per_capita"] = np.log1p(
    wide["gdp_per_capita_usd"]
)


# -------------------------
# Normalization function
# -------------------------

def normalize(series):

    minimum = series.min()
    maximum = series.max()

    return (
        series - minimum
    ) / (
        maximum - minimum
    )


variables = [
    "internet_users_pct",
    "ict_service_exports_pct",
    "tertiary_enrolment_pct",
    "log_gdp_per_capita"
]


score_columns = []

for variable in variables:

    score_name = f"{variable}_score"

    wide[score_name] = normalize(
        wide[variable]
    )

    score_columns.append(
        score_name
    )


# -------------------------
# Composite indicator
# -------------------------

wide[
    "components_available"
] = wide[
    score_columns
].notna().sum(
    axis=1
)


wide[
    "readiness_index"
] = (
    wide[
        score_columns
    ].mean(
        axis=1,
        skipna=True
    )
    * 100
)


# Require at least 3 components

wide.loc[
    wide["components_available"] < 3,
    "readiness_index"
] = np.nan


# -------------------------
# Save
# -------------------------

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

wide.to_csv(
    OUTPUT,
    index=False
)


print("Processing complete")
print(f"Rows: {len(wide)}")
print(f"Countries: {wide['country_code'].nunique()}")
print(f"Saved to: {OUTPUT}")