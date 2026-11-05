import os
from bs4 import BeautifulSoup
import json
from http_client import get as http_get, search_pickles


def call_auction(auction_id):
    url = f"https://www.pickles.com.au/api-website/buyer/ms-web-asset-search/v2/api/product/public/{auction_id}/search"
    response = search_pickles(url, top=100)
    return(response)


def call_car_list(fields):
    url = "https://www.pickles.com.au/api-website/buyer/ms-web-asset-search/v2/api/product/public/search"
    per_page = 120
    car_list = []
    skip = 0
    while True:
        response = search_pickles(url, skip=skip, top=per_page, filter="productTypeFilter eq 'cars'", fields=fields)
        res_json = response.get("data", response)
        car_list.extend(res_json["value"])
        if len(res_json["value"]) < per_page:
            break
        skip += per_page
    return car_list

fields = "stockNumber,title,year,make,model,badge,odometer,body,salvage,wovr,buyMethod,price,productBidEnd"
data = call_car_list(fields)

print(len(data))
print(data[0:2])