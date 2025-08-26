from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, OnSiteOrRemoteFilters
import logging

# Change root logger level (default is WARN)
logging.basicConfig(level = logging.INFO)

def on_data(data: EventData):
    with open('linkedin_jobs.html', 'a') as f:
        f.write(f"""
        <div class="job">
            <h2>{data.title}</h2>
            <p><strong>Company:</strong> {data.company}</p>
            <p><strong>Date:</strong> {data.date}</p>
            <p><strong>Location:</strong> {data.location}</p>
            <a href="{data.link}" target="_blank">Apply</a>
            <div class="description">
                {data.description}
            </div>
        </div>
        """)

def on_error(error):
    print('[ON_ERROR]', error)

def on_end():
    print('[ON_END]')

def search_linkedin_jobs(query, location):
    scraper = LinkedinScraper(
        chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chrome) 
        chrome_options=None,  # Custom Chrome options here
        headless=True,  # Overrides headless mode only if chrome_options is None
        max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
        slow_mo=1,  # Slow down processing queries (in seconds)
        page_load_timeout=40  # Page load timeout (in seconds)    
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
                limit=5,
                filters=QueryFilters(
                    relevance=RelevanceFilters.RELEVANT,
                    time=TimeFilters.MONTH,
                    type=[TypeFilters.FULL_TIME],
                    on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE],
                    experience=[ExperienceLevelFilters.MID_SENIOR]
                )
            )
        ),
    ]

    scraper.run(queries)

def create_html_file():
    with open('linkedin_jobs.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
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
</body>
</html>""")

if __name__ == "__main__":
    create_html_file()
    search_query = "Linux System Administrator"
    search_location = "Philippines"
    search_linkedin_jobs(search_query, search_location)
