# Job Search Scripts

Small Python utilities to search job postings from LinkedIn, Indeed, and JobStreet.

## Setup

- Python 3.9+
- Chrome/Chromium installed (for `linkedin-jobs-scraper`)

Install dependencies:

```
pip install -r requirements.txt
```

## LinkedIn Scraper

Generates a simple HTML page (`linkedin_jobs.html`) with job cards.

Usage:

```
python job_search.py \
  --query "Linux System Administrator" \
  --location "Philippines" \
  --limit 5 \
  --html-out linkedin_jobs.html \
  --json-out linkedin_jobs.json
```

Notes:
- Requires Chrome/Chromium available on your system path.
- Writes HTML header first and closes at the end. Also emits a JSON array of jobs.
- Use `--no-html` to skip HTML generation.

## Indeed & JobStreet Scraper

Prints jobs to the console. Selectors are best-effort and may break if sites change.

Usage:

```
python indeed_jobstreet_search.py \
  --query "Linux System Administrator" \
  --location "Philippines" \
  --limit 10 \
  --timeout 15 \
  --json-out jobs.json
```

Notes:
- Includes basic timeouts and error handling. Selectors use best-effort, resilient patterns with fallbacks.
- Respect each site's Terms of Service and robots policies. This code is for educational use only.
