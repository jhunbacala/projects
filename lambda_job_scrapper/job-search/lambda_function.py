import os
import json
import logging
import requests
from bs4 import BeautifulSoup
from time import sleep
from requests.exceptions import HTTPError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

JOB_QUERY    = os.getenv("JOB_QUERY", "Linux System Administrator")
JOB_LOCATION = os.getenv("JOB_LOCATION", "Philippines")
MAX_RESULTS  = int(os.getenv("MAX_RESULTS", "10"))

# A realistic browser User-Agent
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

def build_search_url(query: str, location: str) -> str:
    q = requests.utils.quote(query)
    loc = requests.utils.quote(location)
    return f"https://ph.indeed.com/jobs?q={q}&l={loc}"

def parse_listings(html: str, max_results: int):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="job_seen_beacon")
    results = []
    for card in cards[:max_results]:
        title_el   = card.find("h2", class_="jobTitle")
        comp_el    = card.find("span", class_="companyName")
        link_el    = card.find("a", href=True)
        title      = title_el.get_text(strip=True) if title_el else "N/A"
        company    = comp_el.get_text(strip=True)  if comp_el else "N/A"
        raw_href   = link_el["href"]               if link_el else ""
        link       = f"https://ph.indeed.com{raw_href}"
        results.append({"title": title, "company": company, "link": link})
    return results

def lambda_handler(event, context):
    url = build_search_url(JOB_QUERY, JOB_LOCATION)
    logger.info(f"Searching: {url}")
    
    # Simple retry loop
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            break
        except HTTPError as e:
            logger.warning(f"Attempt {attempt+1} failed: {e}")
            if attempt < 2:
                sleep(2 ** attempt)
            else:
                # Give up after 3 attempts
                return {
                    "statusCode": resp.status_code if 'resp' in locals() else 500,
                    "body": json.dumps({"error": str(e)})
                }
    
    listings = parse_listings(resp.text, MAX_RESULTS)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "query":    JOB_QUERY,
            "location": JOB_LOCATION,
            "results":  listings
        })
    }
