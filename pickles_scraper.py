import os
from bs4 import BeautifulSoup
import json
from http_client import get as http_get, search_pickles


auction_id = 16542
url = f"https://www.pickles.com.au/api-website/buyer/ms-web-asset-search/v2/api/product/public/{auction_id}/search"
response = search_pickles(url)
print(response)
