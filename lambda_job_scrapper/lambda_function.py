import os
import json
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Read from Lambda environment or default to Philippines
JOB_QUERY    = os.getenv("JOB_QUERY", "Linux System Administrator")
JOB_LOCATION = os.getenv("JOB_LOCATION", "Philippines")
MAX_RESULTS  = int(os.getenv("MAX_RESULTS", "10"))

def build_search_url(query: str, location: str) -> str:
    """
    Constructs the Indeed.ph search URL for the given query and location.
    """
    q = requests.utils.quote(query)
    loc = requests.utils.quote(location)
    return f"https://ph.indeed.com/jobs?q={q}&l={loc}"

def parse_listings(html: str, max_results: int):
    """
    Parses the first max_results job cards from Indeed search results.
    """
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="job_seen_beacon")  # Indeed's current card class
    results = []

    for card in cards[:max_results]:
        # Title
        title_el = card.find("h2", class_="jobTitle")
        title = title_el.get_text(strip=True) if title_el else "N/A"

        # Company
        comp_el = card.find("span", class_="companyName")
        company = comp_el.get_text(strip=True) if comp_el else "N/A"

        # Link
        link_el = card.find("a", href=True)
        raw_href = link_el["href"] if link_el else ""
        link = f"https://ph.indeed.com{raw_href}"

        results.append({
            "title":   title,
            "company": company,
            "link":    link
        })

    return results

def lambda_handler(event, context):
    """
    Lambda entry point.
    """
    url = build_search_url(JOB_QUERY, JOB_LOCATION)
    logger.info(f"Searching: {url}")

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    listings = parse_listings(resp.text, MAX_RESULTS)

    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps({
            "query":    JOB_QUERY,
            "location": JOB_LOCATION,
            "results":  listings
        })
    }
