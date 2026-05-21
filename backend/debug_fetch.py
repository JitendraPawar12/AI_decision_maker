from app.utils.env import load_environment
from app.services.serp_api_service import fetch_shopping_listings
import time

load_environment()
start = time.time()
try:
    listings = fetch_shopping_listings('iPhone 15')
    print('LISTINGS', len(listings))
    if listings:
        print(listings[0].dict())
except Exception as e:
    print('ERROR', type(e).__name__, e)
print('ELAPSED', time.time() - start)
