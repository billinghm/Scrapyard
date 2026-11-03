import base64, json
from curl_cffi import requests, CurlOpt

URL = "https://www.pickles.com.au/api-website/buyer/ms-web-asset-search/v2/api/product/public/16518/search"

def search(skip=0, top=30, filter=""):
    query = {"search": "*", "count": True, "top": top, "skip": skip, "orderby": "", "filter": filter}
    body = {"data": base64.b64encode(json.dumps(query).encode()).decode()}
    r = requests.post(URL, json=body, headers={"x-encode-base64": "true"}, impersonate="chrome", curl_options={CurlOpt.DNS_SERVERS: "1.1.1.1,8.8.8.8"})
    r.raise_for_status()
    return r.json()

print(json.dumps(search(), indent=2)[:2000])