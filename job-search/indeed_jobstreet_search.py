import requests
from bs4 import BeautifulSoup

def search_indeed(query, location='Philippines'):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://ph.indeed.com/jobs?q={query}&l={location}"
    resp = requests.get(url, headers=headers)
    jobs = []
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        cards = soup.select('.jobsearch-SerpJobCard')
        for card in cards[:10]:
            title = card.select_one('.title a').get_text(strip=True)
            company = card.select_one('.company').get_text(strip=True)
            loc = card.select_one('.location').get_text(strip=True)
            link = 'https://ph.indeed.com' + card.select_one('.title a')['href']
            jobs.append((title, company, loc, link))
    return jobs

def search_jobstreet(query, location='Philippines'):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://www.jobstreet.com.ph/en/job-search/{query}-jobs-in-{location}"
    resp = requests.get(url, headers=headers)
    jobs = []
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        cards = soup.select('.sx2jih0.zcydq84u')
        for card in cards[:10]:
            title = card.select_one('a').get_text(strip=True)
            company = card.select_one('.sx2jih0._18qlyvc0').get_text(strip=True)
            loc = card.select_one('.sx2jih0._14mejww').get_text(strip=True)
            link = 'https://www.jobstreet.com.ph' + card.select_one('a')['href']
            jobs.append((title, company, loc, link))
    return jobs

if __name__ == '__main__':
    query = 'Linux System Administrator'
    all_jobs = search_indeed(query) + search_jobstreet(query)
    for title, company, loc, link in all_jobs:
        print(f"{title} | {company} | {loc}\n→ {link}\n{'-'*40}")
