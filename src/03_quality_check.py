from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "country_year_indicators.csv"
)

OUTPUT = (
    PROJECT_ROOT
    / "reports"
    / "quality_report.csv"
)


df = pd.read_csv(INPUT)

report = []


def add_metric(metric, value):
    report.append({
        "metric": metric,
        "value": value
    })


add_metric(
    "number_of_rows",
    len(df)
)

add_metric(
    "number_of_countries",
    df["country_code"].nunique()
)

add_metric(
    "minimum_year",
    df["year"].min()
)

add_metric(
    "maximum_year",
    df["year"].max()
)


duplicates = df.duplicated(
    subset=[
        "country_code",
        "year"
    ]
).sum()

add_metric(
    "duplicate_country_year",
    duplicates
)


for column in df.columns:

    missing = (
        df[column]
        .isna()
        .mean()
        * 100
    )

    add_metric(
        f"missing_pct_{column}",
        round(missing, 2)
    )


report_df = pd.DataFrame(report)


OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

report_df.to_csv(
    OUTPUT,
    index=False
)


print(report_df.to_string(index=False))

print()
print(
    f"Quality report saved to {OUTPUT}"
)