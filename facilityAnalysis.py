
import pandas as pd
import matplotlib.pyplot as plt

NUMERIC_COLS = ["cleanliness_score", "odor_score", "footfall", "complaints"]


def load_data(path="facility_data.csv"):
    """Read the CSV and parse the date column so pandas treats it as a real date."""
    return pd.read_csv(path, parse_dates=["inspection_date"])


def audit_data(df):
    """
    Count problems WITHOUT changing anything yet.
    Returns a dict report so we know exactly what was wrong before we fix it.
    """
    invalid_scores = (
        (df["cleanliness_score"] < 0) | (df["cleanliness_score"] > 10) |
        (df["odor_score"] < 0) | (df["odor_score"] > 10)
    )
    return {
        "missing_values": df.isna().sum().to_dict(),
        "duplicate_facility_ids": int(df.duplicated("facility_id").sum()),
        "negative_footfall": int((df["footfall"] < 0).sum()),
        "out_of_range_scores": int(invalid_scores.sum()),
    }


def clean_data(df):
    """
    Fix the problems audit_data() found:
    - drop duplicate facilities (keep first occurrence)
    - turn impossible values (negative footfall) into NaN
    - fill remaining NaNs with the column median (robust to outliers, unlike mean)
    """
    df = df.drop_duplicates("facility_id").copy()
    df.loc[df["footfall"] < 0, "footfall"] = pd.NA
    df[NUMERIC_COLS] = df[NUMERIC_COLS].apply(lambda col: col.fillna(col.median()))
    return df


def find_outliers(df):
    """
    IQR method: a value is an outlier if it falls outside
    [Q1 - 1.5*IQR, Q3 + 1.5*IQR]. Standard, robust, no distribution assumptions.
    """
    outlier_counts = {}
    for col in NUMERIC_COLS:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outlier_counts[col] = int(((df[col] < lower) | (df[col] > upper)).sum())
    return outlier_counts


def summarize(df):
    """Key descriptive stats overall, and averages broken down by location."""
    overall = df[NUMERIC_COLS].describe().T[["mean", "std", "min", "50%", "max"]].round(2)
    by_location = df.groupby("location")[NUMERIC_COLS].mean().round(2)
    return overall, by_location


def generate_insights(df, by_location):
    """Turn the numbers into three plain-English takeaways."""
    worst_location = by_location["cleanliness_score"].idxmin()
    correlation = df["cleanliness_score"].corr(df["complaints"])
    pct_no_water = (df["water_availability"] == "No").mean() * 100

    return [
        f"'{worst_location}' has the lowest avg cleanliness score "
        f"({by_location['cleanliness_score'].min():.2f}) — needs priority attention.",

        f"Cleanliness vs complaints correlation = {correlation:.2f} "
        f"({'cleaner facilities get fewer complaints' if correlation < 0 else 'little to no linear relation'}).",

        f"{pct_no_water:.1f}% of facilities lack water availability — a direct hygiene risk.",
    ]


def make_charts(df, by_location, out_path="facility_analysis.png"):
    """Five charts covering the required types: 2 bar, 1 histogram, 1 scatter, 1 extra (pie)."""
    fig, ax = plt.subplots(2, 3, figsize=(16, 9))

    by_location["cleanliness_score"].sort_values().plot.bar(
        ax=ax[0, 0], color="teal", title="Avg Cleanliness Score by Location")

    df["waste_level"].value_counts().plot.bar(
        ax=ax[0, 1], color="orange", title="Facility Count by Waste Level")

    df["cleanliness_score"].plot.hist(
        ax=ax[0, 2], bins=15, color="slateblue", title="Cleanliness Score Distribution")

    ax[1, 0].scatter(df["footfall"], df["complaints"], alpha=0.5, c=df["odor_score"], cmap="Reds")
    ax[1, 0].set(title="Footfall vs Complaints (color = odor)", xlabel="Footfall", ylabel="Complaints")

    weekly_trend = df.set_index("inspection_date").sort_index()["cleanliness_score"].resample("W").mean()
    weekly_trend.plot(ax=ax[1, 1], title="Weekly Avg Cleanliness Trend")

    df["water_availability"].value_counts().plot.pie(
        ax=ax[1, 2], autopct="%1.0f%%", title="Water Availability")

    for a in ax.flat:
        a.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    print(f"Saved charts -> {out_path}")


def main():
    df = load_data()

    quality_report = audit_data(df)      # what's wrong, before touching the data
    df = clean_data(df)                  # fix it
    quality_report["outliers"] = find_outliers(df)

    overall_stats, by_location = summarize(df)
    insights = generate_insights(df, by_location)

    print("=== DATA QUALITY REPORT ===")
    for key, value in quality_report.items():
        print(f"{key}: {value}")

    print("\n=== KEY STATISTICS ===\n", overall_stats)
    print("\n=== AVERAGES BY LOCATION ===\n", by_location)

    print("\n=== INSIGHTS ===")
    for i, point in enumerate(insights, 1):
        print(f"{i}. {point}")

    make_charts(df, by_location)


if __name__ == "__main__":
    main()