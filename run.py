import sys
import os
from datetime import datetime
from backend.llm_writer import generate_cover_letter

if len(sys.argv) < 4:
    print("Usage: python run.py <job_title> <company_name> <job_description>")
    sys.exit(1)

job_title = sys.argv[1]
company_name = sys.argv[2]
job_description = sys.argv[3]

# Replace this with your base background or load from a file
user_background = "MBA at McGill, ex-BMO Delivery Lead, built AI startup Aemete, taught business analysis, led $45M platform migration."

letter = generate_cover_letter(job_title, company_name, job_description, user_background)

# Add bot disclaimer
letter += "\n\n—\nThis job was applied to by a custom AI job bot I built to showcase my engineering skills and automate high-quality applications."

# Output
print("\n=== Cover Letter ===\n")
print(letter)

# Save to file
os.makedirs("data/cover_letters", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = f"data/cover_letters/cover_letter_{timestamp}.txt"
with open(file_path, "w") as f:
    f.write(letter)

print(f"\n✅ Saved to: {file_path}")