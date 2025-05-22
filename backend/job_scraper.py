import requests
import json

# Greenhouse job board scraper
def scrape_greenhouse(company_slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"[ERROR] Could not fetch jobs for {company_slug}")
        return []

    jobs = response.json().get("jobs", [])
    return [
        {
            "company": company_slug,
            "title": job["title"],
            "location": job["location"]["name"] if job.get("location") else "N/A",
            "url": job["absolute_url"]
        }
        for job in jobs
    ]


# Lever job board scraper
def scrape_lever(company_slug):
    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"[ERROR] Could not fetch jobs for {company_slug}")
        return []

    jobs = response.json()
    return [
        {
            "company": company_slug,
            "title": job["text"],
            "location": job["categories"].get("location", "N/A"),
            "url": job["hostedUrl"]
        }
        for job in jobs
    ]


# Combined runner
def run_scraper():
    greenhouse_companies = ["stripe", "asana", "robinhood"]
    lever_companies = ["airtable", "samsara", "nylas"]

    all_jobs = []

    for company in greenhouse_companies:
        all_jobs.extend(scrape_greenhouse(company))

    for company in lever_companies:
        all_jobs.extend(scrape_lever(company))

    print(f"[INFO] Total jobs scraped: {len(all_jobs)}")

    with open("data/jobs_raw.json", "w") as f:
        json.dump(all_jobs, f, indent=2)


# Run only when script is called directly
if __name__ == "__main__":
    run_scraper()