import os
import openai
from backend.config import (
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT_NAME,
    AZURE_OPENAI_API_VERSION
)

# This file handles only GPT-based rewriting of cover letters and resumes.
# Formatting preservation (e.g., header/footer retention, .docx cloning) should be done outside, in the calling module.

# --- Azure OpenAI Configuration ---
openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = AZURE_OPENAI_API_VERSION
openai.api_key = AZURE_OPENAI_KEY


# --- Load role-specific prompt template ---
def load_prompt_template(role_category):
    path = {
        "finance": "backend/utils/prompt_finance.txt",
        "pm_tech": "backend/utils/prompt_pm_tech.txt"
    }.get(role_category, "backend/utils/prompt_pm_tech.txt")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt template not found: {path}")

    with open(path, "r") as f:
        return f.read()


# --- Generate Cover Letter Body using GPT ---
def generate_cover_letter(job_title, company_name, job_description, user_background, system_prompt):
    user_prompt = f"""
This job was applied using an AI bot I built to automate job applications and demonstrate my product thinking, engineering skills, and initiative.

Write only the body paragraphs of a cover letter for the position of {job_title} at {company_name}.

Here is the job description:
\"\"\"
{job_description}
\"\"\"

Here is the candidate’s background:
\"\"\"
{user_background}
\"\"\"

The tone should match the template and company culture.
Do NOT include header, greeting, closing, or signature.
Return only the main content paragraphs.
"""

    try:
        response = openai.ChatCompletion.create(
            engine=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"[ERROR] GPT failed: {e}")
        return None


# --- Resume Sentence Rewriter (Minimal Edits, Preserve Formatting Tags) ---
def rewrite_resume_sentences(lines, job_metadata):
    # Note for developers: This function expects minimal sentence-level edits only.
    # It preserves formatting tags and structure as-is.
    # Actual DOCX copy-pasting and formatting preservation is handled outside this function.
    prompt = f"""
You are an AI assistant improving a resume with minimal sentence-level edits.

You will receive lines from a resume. Rewrite each line to better match this job:

Job Metadata:
{job_metadata}

Rules:
- Make only minimal improvements or keyword substitutions
- Preserve all formatting tags and structure exactly as in the original lines
- Do NOT summarize, rearrange, or remove content
- Return one revised line per input line

Respond with the improved lines in the same order, separated by new lines.
"""

    input_text = "\n".join(lines)

    try:
        response = openai.ChatCompletion.create(
            engine=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a precise resume enhancer."},
                {"role": "user", "content": prompt + "\n\nResume Lines:\n" + input_text}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        return response["choices"][0]["message"]["content"].splitlines()

    except Exception as e:
        print(f"[ERROR] Resume rewriting failed: {e}")
        return lines  # Fallback to original