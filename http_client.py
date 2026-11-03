"""Shared HTTP client for scrapers that hit bot-protected sites.

CapitolTrades sits behind Vercel's bot challenge, which fingerprints the TLS
handshake (JA3/JA4). A plain ``requests`` call from Linux presents a
server-typical OpenSSL fingerprint that gets a ``429`` challenge, while the same
call from a Windows Python (different bundled OpenSSL) happens to pass — which is
why the scraper worked locally but failed on the server despite the same IP.

``curl_cffi`` with ``impersonate="chrome"`` replays a real Chrome TLS + HTTP/2
fingerprint, so the request looks like the browser that already works.

We import it defensively: if ``curl_cffi`` isn't installed we fall back to plain
``requests`` so the app still imports and runs (it just may hit the challenge)
in an environment that hasn't installed the optional dependency — keeping the
app runnable both standalone and inside the portal.
"""
import requests as _requests
import base64, json

try:
    from curl_cffi import requests as _cffi, CurlOpt
    _USING_CFFI = True
except Exception:  # pragma: no cover - depends on the environment
    _USING_CFFI = False

# Browser build to impersonate (TLS + header fingerprint).
_IMPERSONATE = "chrome"

# Only used for the plain-requests fallback; curl_cffi supplies its own
# browser-consistent headers via impersonate.
_FALLBACK_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

DEFAULT_TIMEOUT = 30


def get(url, **kwargs):
    """GET a URL with a browser-like fingerprint.

    Returns a requests-compatible response (``.status_code``, ``.text``,
    ``.raise_for_status()``), whether backed by curl_cffi or requests.
    """
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    if _USING_CFFI:
        # impersonate provides a full, self-consistent Chrome header + TLS set;
        # don't override its User-Agent.
        return _cffi.get(url, impersonate=_IMPERSONATE, **kwargs,  curl_options={CurlOpt.DNS_SERVERS: "1.1.1.1,8.8.8.8"})
    kwargs.setdefault("headers", _FALLBACK_HEADERS)
    return _requests.get(url, **kwargs)


def search_pickles(url, skip=0, top=30, filter=""):
    query = {"search": "*", "count": True, "top": top, "skip": skip, "orderby": "", "filter": filter}
    body = {"data": base64.b64encode(json.dumps(query).encode()).decode()}
    headers = {"x-encode-base64": "true"} 
    if _USING_CFFI:
         # impersonate provides a full, self-consistent Chrome header + TLS set;
         # don't override its User-Agent.
        r = _cffi.post(url, impersonate=_IMPERSONATE, json=body, headers=headers,  curl_options={CurlOpt.DNS_SERVERS: "1.1.1.1,8.8.8.8"})
        return r.json()
    r = _requests.post(url, json=body, headers=headers)
    r.raise_for_status()
    return r.json()
