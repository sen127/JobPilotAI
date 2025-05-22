import os
import openai
from backend.config import (
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT_NAME,
    AZURE_OPENAI_API_VERSION
)

openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = AZURE_OPENAI_API_VERSION
openai.api_key = AZURE_OPENAI_KEY


def generate_cover_letter(job_title, company_name, job_description, user_background):
    system_prompt = (
        f"You are a professional career assistant who writes concise, tailored, and compelling cover letters "
        f"for MBA candidates applying to roles in consulting, strategy, and finance. Highlight their technical "
        f"and business experience clearly, matching them to the job description."
    )

    user_prompt = f"""
Write a cover letter for the position of {job_title} at {company_name}.

Here is the job description:
\"\"\"
{job_description}
\"\"\"

Here is the candidate’s background:
\"\"\"
{user_background}
\"\"\"

The tone should be confident, concise, and results-oriented.
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

        return response['choices'][0]['message']['content']

    except Exception as e:
        print(f"[ERROR] GPT failed: {e}")
        return None