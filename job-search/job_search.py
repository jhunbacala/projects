from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import (
    RelevanceFilters,
    TimeFilters,
    TypeFilters,
    ExperienceLevelFilters,
    OnSiteOrRemoteFilters,
)
import logging
import argparse
import json

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)

# Runtime context shared with event handlers
_CTX = {
    'collect': [],
    'html_enabled': True,
    'html_path': 'linkedin_jobs.html',
    'json_path': 'linkedin_jobs.json',
}


def on_data(data: EventData):
    # Collect for JSON
    _CTX['collect'].append({
        'title': data.title,
        'company': data.company,
        'date': str(data.date),
        'location': data.location,
        'link': data.link,
        'description': data.description,
        'source': 'linkedin',
    })

    # Append each job card inside the open <body>
    if _CTX['html_enabled']:
        with open(_CTX['html_path'], 'a', encoding='utf-8') as f:
            f.write(
                f"""
        <div class=\"job\">\n            <h2>{data.title}</h2>\n            <p><strong>Company:</strong> {data.company}</p>\n            <p><strong>Date:</strong> {data.date}</p>\n            <p><strong>Location:</strong> {data.location}</p>\n            <a href=\"{data.link}\" target=\"_blank\">Apply</a>\n            <div class=\"description\">\n                {data.description}\n            </div>\n        </div>\n        """
            )


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    # Close the HTML document properly at the end
    if _CTX['html_enabled']:
        with open(_CTX['html_path'], 'a', encoding='utf-8') as f:
            f.write("\n</body>\n</html>\n")

    # Write JSON output
    try:
        with open(_CTX['json_path'], 'w', encoding='utf-8') as jf:
            json.dump(_CTX['collect'], jf, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ON_END] Failed to write JSON: {e}")

    print('[ON_END]')


def search_linkedin_jobs(query, location, limit=5):
    scraper = LinkedinScraper(
        chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chrome)
        chrome_options=None,  # Custom Chrome options here
        headless=True,  # Overrides headless mode only if chrome_options is None
        max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
        slow_mo=1,  # Slow down processing queries (in seconds)
        page_load_timeout=40,  # Page load timeout (in seconds)
    )

    # Add event listeners
    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    queries = [
        Query(
            query=query,
            options=QueryOptions(
                locations=[location],
                apply_link=True,  # Try to extract apply link
                skip_promoted_jobs=True,  # Skip promoted jobs
                page_offset=0,  # How many pages to skip
                limit=limit,
                filters=QueryFilters(
                    relevance=RelevanceFilters.RELEVANT,
                    time=TimeFilters.MONTH,
                    type=[TypeFilters.FULL_TIME],
                    on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE],
                    experience=[ExperienceLevelFilters.MID_SENIOR],
                ),
            ),
        ),
    ]

    scraper.run(queries)


def create_html_file(path: str):
    # Write opening HTML (no closing tags). Jobs will be appended, and tags closed on on_end().
    with open(path, 'w', encoding='utf-8') as f:
        f.write(
            """<!DOCTYPE html>
<html>
<head>
    <meta charset=\"utf-8\" />
    <title>LinkedIn Jobs</title>
    <style>
        body {
            font-family: sans-serif;
            margin: 20px;
        }
        .job {
            border: 1px solid #ccc;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        .job h2 {
            margin-top: 0;
        }
        .job a {
            display: inline-block;
            background-color: #007bff;
            color: #fff;
            padding: 8px 12px;
            text-decoration: none;
            border-radius: 3px;
            margin-top: 10px;
        }
        .description {
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <h1>LinkedIn Job Postings</h1>
"""
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn job scraper -> HTML/JSON")
    parser.add_argument("--query", default="Linux System Administrator", help="Search keywords")
    parser.add_argument("--location", default="Philippines", help="Job location")
    parser.add_argument("--limit", type=int, default=5, help="Max jobs to fetch")
    parser.add_argument("--html-out", default="linkedin_jobs.html", help="HTML output path")
    parser.add_argument("--json-out", default="linkedin_jobs.json", help="JSON output path")
    parser.add_argument("--no-html", action="store_true", help="Disable HTML output")
    args = parser.parse_args()

    _CTX['html_enabled'] = not args.no_html
    _CTX['html_path'] = args.html_out
    _CTX['json_path'] = args.json_out

    if _CTX['html_enabled']:
        create_html_file(_CTX['html_path'])
    search_linkedin_jobs(args.query, args.location, args.limit)

