import time

import httpx
from selectolax.parser import HTMLParser

from module.common import calculate_hash

MAX_RETRIES = 10
RETRY_DELAY_SECONDS = 5
TIMEOUT = 100


def get_html(site, path):
    url = site + path
    retries = 0

    while retries < MAX_RETRIES:
        try:
            resp = httpx.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
            return HTMLParser(resp.text)
        except httpx.RequestError as err:
            print(f"[Error] HTTP request: {err}")
        except httpx.HTTPStatusError as err:
            print(f"[Error] HTTP status: {err}")

        retries += 1
        if retries < MAX_RETRIES:
            print(f"[Info] Retrying in {RETRY_DELAY_SECONDS * retries} seconds...")
            time.sleep(RETRY_DELAY_SECONDS * retries)

    print(f"[Info] Max retries exceeded. Unable to get HTML from {url}.")
    return None


def extract(html, selector, option, index=None):
    element = html.css_first(selector)
    if element is not None:
        if option == 'text':
            return element.text(strip=True)
        elif option == 'attrs':
            return element.attributes
        elif option == 'hash':
            element = html.css(selector)[index]
            return calculate_hash(element.attributes['href'])
        else:
            return element
