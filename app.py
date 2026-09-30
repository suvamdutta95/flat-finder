from pathlib import Path
import pandas as pd
import streamlit as st
from flat_finder.dedupe import dedupe_listings
from flat_finder.filters import filter_listings
from flat_finder.providers.csv_provider import CSVListingProvider

st.set_page_config(page_title="Kolkata Flat Finder", page_icon="🏠", layout="wide")
DATA_FILE = Path("data/sample_listings.csv")

@st.cache_data
def load_demo_listings() -> pd.DataFrame:
    items = dedupe_listings(CSVListingProvider(DATA_FILE).load())
    return pd.DataFrame([item.to_dict() for item in items])

st.markdown("""<style>
.hero{padding:1.6rem 1.8rem;border-radius:18px;background:linear-gradient(135deg,#111827,#1f2937);color:white;margin-bottom:1.2rem}
.hero h1{margin:0 0 .35rem}.hero p{margin:0;opacity:.86}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🏠 Kolkata Flat Finder</h1><p>Tell us what you need. We will make the shortlist simple.</p></div>', unsafe_allow_html=True)

df = load_demo_listings()
with st.sidebar:
    st.header("🔎 Search")
    purpose = st.radio("I want to", ["Any","Rent","Buy"], horizontal=True)
    locality = st.selectbox("Where?", ["Any"] + sorted(df["locality"].unique().tolist()))
    bhk = st.selectbox("BHK", ["Any"] + sorted(df["bhk"].unique().tolist()))
    pmin, pmax = int(df["price_inr"].min()), int(df["price_inr"].max())
    min_budget, max_budget = st.slider("Budget (₹)", pmin, pmax, (pmin, pmax), step=50000)
    min_area = st.slider("Minimum area (sq ft)", 0, int(df["area_sqft"].max()), 0, step=100)
    furnishing = st.selectbox("Furnishing", ["Any","Unfurnished","Semi-Furnished","Fully Furnished"])
    only_new = st.checkbox("🆕 Newly listed (last 7 days)")
    parking = st.checkbox("🚗 Parking required")
    lift = st.checkbox("🛗 Lift required")
    keyword = st.text_input("Keyword", placeholder="e.g. New Town, balcony, metro...")

results = filter_listings(df, purpose=purpose, locality=locality, bhk=bhk,
    min_price=min_budget, max_price=max_budget, min_area=min_area,
    furnishing=furnishing, parking=parking, lift=lift,
    only_new=only_new, keyword=keyword)

st.subheader(f"{len(results)} matching listing(s)")
if results.empty:
    st.info("No matching listings in the current dataset. Try widening one or two filters.")
else:
    display = results.copy()
    display["Price"] = display.apply(lambda r: f"₹{r['price_inr']:,.0f}" if r["purpose"]=="Buy" else f"₹{r['price_inr']:,.0f}/month", axis=1)
    display["Area"] = display["area_sqft"].map(lambda x: f"{x:,.0f} sq ft")
    display["Posted"] = pd.to_datetime(display["posted_at"]).dt.strftime("%d %b %Y")
    table = display[["title","locality","bhk","Area","Price","furnishing","Posted","source","url"]].rename(
        columns={"title":"Listing","locality":"Locality","bhk":"BHK","furnishing":"Furnishing","source":"Source","url":"Link"})
    st.dataframe(table, use_container_width=True, hide_index=True,
        column_config={"Link": st.column_config.LinkColumn("View listing")})
    c1,c2=st.columns(2)
    with c1:
        st.download_button("⬇️ Download CSV", display.to_csv(index=False).encode(), "kolkata-flat-results.csv", "text/csv")
    with c2:
        st.download_button("⬇️ Download JSON", display.to_json(orient="records", indent=2).encode(), "kolkata-flat-results.json", "application/json")
st.caption("Demo mode uses local sample data. Production sources should be authorized APIs, feeds, or datasets.")
