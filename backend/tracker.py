

import json
from pathlib import Path
from datetime import datetime

class JobTracker:
    def __init__(self, user_dir):
        self.log_path = Path(user_dir) / "application_tracker.json"
        if not self.log_path.exists():
            self._init_log()

    def _init_log(self):
        with open(self.log_path, "w") as f:
            json.dump({"applications": []}, f, indent=2)

    def log_status(self, job_title, company, status, job_url):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "job_title": job_title,
            "company": company,
            "status": status,  # e.g., "scraped", "applied", "failed"
            "timestamp": timestamp,
            "job_url": job_url
        }
        with open(self.log_path, "r+") as f:
            data = json.load(f)
            data["applications"].append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

    def get_all_applications(self):
        with open(self.log_path) as f:
            return json.load(f)["applications"]