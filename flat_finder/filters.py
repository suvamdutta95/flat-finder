from datetime import datetime, timedelta, timezone
import pandas as pd

def filter_listings(
    df: pd.DataFrame, *, purpose="Any", locality="Any", bhk="Any",
    min_price=None, max_price=None, min_area=0, furnishing="Any",
    parking=False, lift=False, only_new=False, keyword=""
) -> pd.DataFrame:
    result = df.copy()
    if purpose != "Any":
        result = result[result["purpose"].str.casefold() == purpose.casefold()]
    if locality != "Any":
        result = result[result["locality"] == locality]
    if bhk != "Any":
        result = result[result["bhk"] == int(bhk)]
    if min_price is not None:
        result = result[result["price_inr"] >= min_price]
    if max_price is not None:
        result = result[result["price_inr"] <= max_price]
    if min_area:
        result = result[result["area_sqft"] >= min_area]
    if furnishing != "Any":
        result = result[result["furnishing"].str.casefold() == furnishing.casefold()]
    if parking:
        result = result[result["parking"]]
    if lift:
        result = result[result["lift"]]
    if keyword.strip():
        needle = keyword.strip().casefold()
        text = (
            result["title"].fillna("") + " " +
            result["locality"].fillna("") + " " +
            result["property_type"].fillna("")
        ).str.casefold()
        result = result[text.str.contains(needle, regex=False)]
    if only_new:
        dates = pd.to_datetime(result["posted_at"], utc=True, errors="coerce")
        cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        result = result[dates >= cutoff]
    return result.sort_values("posted_at", ascending=False).reset_index(drop=True)
