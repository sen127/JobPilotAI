# JobPilotAI

An experimental Python automation project for collecting job listings and streamlining repetitive parts of the application workflow.

## What it does

- Scrapes job listings from LinkedIn-oriented search flows
- Stores and processes collected opportunities
- Uses browser automation to attempt supported application steps
- Runs the scraping and application stages through a single pipeline

## Tech stack

- Python
- Selenium and browser automation
- Beautiful Soup and HTTP tooling
- Pandas for data handling

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Environment variables and a compatible browser driver may be required depending on the workflow being tested.

## Project status

This is a personal prototype for exploring job-search automation. Website interfaces and anti-automation controls change frequently, so individual workflows may require maintenance and should be used responsibly and in accordance with platform rules.
