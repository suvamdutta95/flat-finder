import pandas as pd
from flat_finder.filters import filter_listings

def sample_df():
    return pd.DataFrame([
        {"title":"New Town 2BHK","locality":"New Town","city":"Kolkata",
         "purpose":"Rent","property_type":"Apartment","bhk":2,"area_sqft":950,
         "price_inr":28000,"furnishing":"Semi-Furnished","parking":True,"lift":True,
         "posted_at":"2026-09-30T07:30:00Z","source":"Test","url":"https://example.com/1"},
        {"title":"Garia 1BHK","locality":"Garia","city":"Kolkata",
         "purpose":"Rent","property_type":"Apartment","bhk":1,"area_sqft":620,
         "price_inr":16000,"furnishing":"Fully Furnished","parking":False,"lift":True,
         "posted_at":"2026-09-10T07:30:00Z","source":"Test","url":"https://example.com/2"},
    ])

def test_filters_by_locality_and_budget():
    result = filter_listings(sample_df(), purpose="Rent", locality="New Town",
                             min_price=20000, max_price=30000)
    assert len(result) == 1
    assert result.iloc[0]["title"] == "New Town 2BHK"

def test_filters_by_parking():
    result = filter_listings(sample_df(), parking=True)
    assert len(result) == 1
    assert bool(result.iloc[0]["parking"]) is True
