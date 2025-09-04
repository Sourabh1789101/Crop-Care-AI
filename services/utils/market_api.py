from datetime import datetime
from typing import Dict, List

# In production, integrate Agmarknet/eNAM official APIs.
# For hackathon, we provide a mock with a few crops and prices.

MOCK_PRICES = [
    {"market": "Ahmedabad (APMC)", "crop": "wheat", "modal_price": 2250, "unit": "INR/qtl"},
    {"market": "Surat (APMC)", "crop": "cotton", "modal_price": 6500, "unit": "INR/qtl"},
    {"market": "Pune (APMC)", "crop": "tomato", "modal_price": 1200, "unit": "INR/qtl"},
    {"market": "Indore (APMC)", "crop": "soybean", "modal_price": 4800, "unit": "INR/qtl"},
]


def get_prices(crop: str | None = None, state: str | None = None) -> Dict:
    items: List[Dict] = MOCK_PRICES
    if crop:
        items = [x for x in items if x["crop"].lower() == crop.lower()]
    # state filtering omitted in mock
    return {"as_of": datetime.utcnow().isoformat() + "Z", "results": items}
