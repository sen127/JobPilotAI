import re
import json
from typing import Dict
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


def extract_metadata_from_jd(jd_text: str) -> Dict:
    """
    Extracts structured metadata from a raw job description using GPT.
    """
    system_prompt = """
You are an AI assistant that extracts structured metadata from raw job descriptions. 
Return a VALID JSON object with the following keys:
- job_title
- company_name
- location
- department
- required_skills (list)
- soft_skills (list)
- tools (list)
- education (list)
- experience (string)
- tone_keywords (list)
- mission_or_values (string)
- reporting_line (string)
- seniority_level (string)
- employment_type (string)

Ensure it's valid JSON (no single quotes, no trailing commas).
"""

    try:
        response = openai.ChatCompletion.create(
            engine=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": jd_text}
            ],
            temperature=0.2,
            max_tokens=800
        )
        raw_json = response['choices'][0]['message']['content']
        metadata = json.loads(raw_json)
        return metadata

    except Exception as e:
        print(f"[ERROR] Failed to extract metadata: {e}")
        return {}