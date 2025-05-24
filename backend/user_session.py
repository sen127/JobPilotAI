import os
from pathlib import Path
from docx import Document

USER_BASE_DIR = "data/users"

def init_user_session():
    print("👋 Welcome to JobPilot.AI")
    username = input("Please enter your username (e.g., BhimMishra): ").strip().replace(" ", "")

    user_dir = Path(USER_BASE_DIR) / username
    resume_path = user_dir / "resume.docx"
    cover_template_path = user_dir / "cover_template.docx"
    prompt_path = user_dir / "prompt.txt"
    os.makedirs(user_dir, exist_ok=True)

    print(f"\n👤 User: {username}")

    # Check for prompt file
    if prompt_path.exists():
        print("📄 Existing prompt found.")
        with open(prompt_path, 'r') as f:
            current_prompt = f.read()
        print("\n--- Your Current Prompt ---\n")
        print(current_prompt)
        print("\n---------------------------\n")
        if input("Would you like to update it? (y/n): ").lower().strip() == 'y':
            print("Paste your prompt. Type EOF (in all caps) on a new line to finish:")
            lines = []
            while True:
                line = input()
                if line.strip() == "EOF":
                    break
                lines.append(line)
            new_prompt = "\n".join(lines)
            with open(prompt_path, 'w') as f:
                f.write(new_prompt)
            print("✅ Prompt updated.")
        else:
            print("👌 Using existing prompt.")
    else:
        print("🆕 No prompt found. Let's create one.")
        print("Paste your prompt. Type EOF (in all caps) on a new line to finish:")
        lines = []
        while True:
            line = input()
            if line.strip() == "EOF":
                break
            lines.append(line)
        with open(prompt_path, 'w') as f:
            f.write("\n".join(lines))
        print("✅ Prompt saved.")

    # Check for resume
    if not resume_path.exists():
        print("📂 Please place your resume at:", resume_path)
    else:
        print("📎 Resume found.")

    # Check for cover letter template
    if not cover_template_path.exists():
        print("📂 Please place your cover letter template at:", cover_template_path)
    else:
        print("📎 Cover letter template found.")

    return {
        "username": username,
        "user_dir": str(user_dir),
        "resume_path": str(resume_path),
        "cover_template_path": str(cover_template_path),
        "prompt_path": str(prompt_path)
    }