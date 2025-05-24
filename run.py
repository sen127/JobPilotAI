import subprocess

print("🔄 Starting full job application pipeline...")

# Step 1: Scrape LinkedIn jobs
print("\n🔍 Running scraper...")
scrape_result = subprocess.run(["python", "scrape_linkedin_jobs.py"])
if scrape_result.returncode != 0:
    print("❌ Scraper failed. Exiting.")
    exit(1)

# Step 2: Auto-apply to scraped jobs
print("\n🚀 Running auto-apply script...")
auto_apply_result = subprocess.run(["python", "auto_apply_jobs.py"])
if auto_apply_result.returncode != 0:
    print("❌ Auto-apply script failed. Please check logs.")
    exit(1)

print("\n✅ Job application process completed successfully.")