# 🏠 Kolkata Flat Finder

A simple, fast property-search app focused on Kolkata. Filter listings by locality, purpose, BHK, budget, area, furnishing, parking, lift and freshness.

> Important: this project is designed for data sources that permit automated access, APIs, feeds, or datasets you are authorized to use. It does not bypass anti-bot controls or scrape sources that prohibit automated extraction.

## Run locally

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The repository includes demo data in `data/sample_listings.csv`, so the interface works without external credentials.

## Add a live source

Implement a provider under `flat_finder/providers/` using the `ListingProvider` interface. Providers should return normalized `Listing` objects. Suitable inputs include official APIs, RSS/Atom feeds, partner feeds with permission, and user-owned CSV/JSON datasets.

Never commit API keys. Use environment variables or Streamlit secrets.

## Features

- Easy Kolkata-focused search
- Rent or buy
- BHK, budget and area filters
- Furnishing, parking and lift filters
- Newly listed filter
- Duplicate removal
- Newest-first sorting
- CSV and JSON export
- Pluggable provider architecture
- Automated tests

## Structure

```text
flat-finder/
├── app.py
├── requirements.txt
├── data/sample_listings.csv
├── flat_finder/
│   ├── models.py
│   ├── filters.py
│   ├── dedupe.py
│   └── providers/
├── tests/
└── .github/workflows/tests.yml
```

Demo listings are not live inventory. Users should independently verify availability, pricing, ownership and property condition before a transaction.
