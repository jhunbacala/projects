import argparse
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin


DEFAULT_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    )
}


def _safe_text(node, default=""):
    return node.get_text(strip=True) if node else default


def search_indeed(query, location='Philippines', limit=10, timeout=15):
    params_q = quote_plus(query)
    params_loc = quote_plus(location)
    url = f"https://ph.indeed.com/jobs?q={params_q}&l={params_loc}"
    jobs = []
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        print(f"[Indeed] Request error: {e}")
        return jobs

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Newer Indeed layout: anchors with class tapItem
    cards = soup.select('a.tapItem')
    for card in cards:
        if len(jobs) >= limit:
            break
        title = _safe_text(card.select_one('h2.jobTitle span[title]')) or _safe_text(card.select_one('h2.jobTitle > span'))
        company = _safe_text(card.select_one('.companyName'))
        loc = _safe_text(card.select_one('.companyLocation'))
        href = card.get('href')
        link = urljoin('https://ph.indeed.com', href) if href else ''
        if title and link:
            jobs.append({
                'title': title,
                'company': company,
                'location': loc,
                'link': link,
                'source': 'indeed',
            })

    # Fallback to older selector if needed
    if not jobs:
        # Try modern container cards
        beacon_cards = soup.select('div.job_seen_beacon')
        for card in beacon_cards:
            if len(jobs) >= limit:
                break
            a = card.select_one('h2.jobTitle a') or card.select_one('a.tapItem')
            title = _safe_text(card.select_one('h2.jobTitle span[title]')) or _safe_text(card.select_one('h2.jobTitle > span'))
            company = _safe_text(card.select_one('.companyName'))
            loc = _safe_text(card.select_one('.companyLocation'))
            href = a.get('href') if a else None
            link = urljoin('https://ph.indeed.com', href) if href else ''
            if title and link:
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': loc,
                    'link': link,
                    'source': 'indeed',
                })

    if not jobs:
        # Very old layout
        old_cards = soup.select('.jobsearch-SerpJobCard')
        for card in old_cards[:limit]:
            a = card.select_one('.title a')
            title = _safe_text(a)
            company = _safe_text(card.select_one('.company'))
            loc = _safe_text(card.select_one('.location'))
            link = urljoin('https://ph.indeed.com', a['href']) if a and a.has_attr('href') else ''
            if title and link:
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': loc,
                    'link': link,
                    'source': 'indeed',
                })

    return jobs


def search_jobstreet(query, location='Philippines', limit=10, timeout=15):
    url = (
        f"https://www.jobstreet.com.ph/en/job-search/{quote_plus(query)}-jobs-in-{quote_plus(location)}"
    )
    jobs = []
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        print(f"[JobStreet] Request error: {e}")
        return jobs

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Prefer data-automation attributes when available
    cards = soup.select('[data-automation=job-card]') or soup.select('article[data-automation], article, div')
    for card in cards:
        if len(jobs) >= limit:
            break
        title_a = (
            card.select_one('[data-automation=job-card-title] a')
            or card.select_one('a[href*="/job/"]')
            or card.select_one('a')
        )
        company_el = (
            card.select_one('[data-automation=job-card-company-name]')
            or card.select_one('[data-automation=company-name]')
        )
        loc_el = (
            card.select_one('[data-automation=job-card-location]')
            or card.select_one('[data-automation=job-card-location-mobile]')
        )
        title = _safe_text(title_a)
        company = _safe_text(company_el)
        loc = _safe_text(loc_el)
        href = title_a.get('href') if title_a else None
        # Only accept links that look like job postings
        if href and '/job/' in href:
            link = urljoin('https://www.jobstreet.com.ph', href)
        else:
            link = ''
        if title and link:
            jobs.append({
                'title': title,
                'company': company,
                'location': loc,
                'link': link,
                'source': 'jobstreet',
            })

    return jobs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search jobs from Indeed and JobStreet')
    parser.add_argument('--query', default='Linux System Administrator', help='Search keywords')
    parser.add_argument('--location', default='Philippines', help='Job location')
    parser.add_argument('--limit', type=int, default=10, help='Max jobs per site')
    parser.add_argument('--timeout', type=int, default=15, help='Request timeout (seconds)')
    parser.add_argument('--json-out', default='', help='Write combined JSON to this path')
    args = parser.parse_args()

    indeed_jobs = search_indeed(args.query, args.location, args.limit, args.timeout)
    jobstreet_jobs = search_jobstreet(args.query, args.location, args.limit, args.timeout)
    all_jobs = indeed_jobs + jobstreet_jobs

    for item in all_jobs:
        print(f"{item['title']} | {item['company']} | {item['location']}\n→ {item['link']}\n{'-'*40}")

    if args.json_out:
        try:
            with open(args.json_out, 'w', encoding='utf-8') as jf:
                json.dump(all_jobs, jf, ensure_ascii=False, indent=2)
            print(f"Saved JSON: {args.json_out}")
        except Exception as e:
            print(f"Failed to write JSON: {e}")
