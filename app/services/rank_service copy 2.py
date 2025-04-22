# from typing import Tuple
# import random
# import re
# import base64


import google.generativeai as genai
from typing import Tuple
import re
import base64
import os
import requests


# Initialize Gemini API
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

from app.config import settings

# genai.configure(api_key=settings.GEMINI_API_KEY)


# Use the Gemini Pro model
# model = genai.GenerativeModel("gemini-pro")


def gemini_score_and_feedback(resume: str, job: str) -> tuple[int, str]:
    prompt = f"""
Compare this resume to the job description and return a numeric score (0-100) and a short feedback summary.

Resume:
{resume}

Job Description:
{job}
"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Extract content safely
        model_output = result["candidates"][0]["content"]["parts"][0]["text"]
        
        # Basic heuristic to extract score from model's output
        import re
        score_match = re.search(r"(\d{1,3})", model_output)
        score = int(score_match.group(1)) if score_match else 50

        return score, model_output

    except Exception as e:
        return 50, f"Error during Gemini call: {str(e)}"


# def gemini_score_and_feedback(resume: str, job: str) -> Tuple[int, str]:
#     prompt = f"""
# You are an AI expert resume evaluator. Given a resume and a job description, give:
# 1. A relevance score between 0 and 100.
# 2. A brief explanation of the match quality.

# Resume:
# {resume}

# Job Description:
# {job}

# Respond in JSON with the format:
# {{
#   "score": int,
#   "feedback": "string"
# }}
# """
#     try:
#         response = model.generate_content(prompt)
#         text = response.text.strip()

#         # Use a regex to extract JSON-like response
#         import json
#         import re

#         json_match = re.search(r"\{.*\}", text, re.DOTALL)
#         if json_match:
#             result = json.loads(json_match.group())
#             return result["score"], result["feedback"]
#         else:
#             return 50, "Could not parse Gemini's response. Defaulting to score 50."
#     except Exception as e:
#         return 50, f"Error during Gemini call: {str(e)}"


# def mock_score_and_feedback(resume: str, job: str) -> Tuple[int, str]:
#     resume = resume.lower()
#     job = job.lower()

#     job_keywords = set(re.findall(r'\b\w+\b', job))
#     resume_words = set(re.findall(r'\b\w+\b', resume))

#     matches = job_keywords.intersection(resume_words)
#     match_count = len(matches)
#     total_keywords = len(job_keywords) or 1

#     score = int((match_count / total_keywords) * 100)
#     score = max(40, min(score, 95))

#     feedback = f"Matched {match_count} out of {total_keywords} keywords. Score: {score}/100."

#     return score, feedback


def photo_check_heuristic(photo_base64: str) -> str:
    def detect_format(b64: str) -> str:
        if b64.startswith("data:image/jpeg"):
            return "jpeg"
        elif b64.startswith("data:image/png"):
            return "png"
        elif b64.startswith("data:image/gif"):
            return "gif"
        return "unknown"

    def estimate_quality(size: int) -> int:
        if size > 30000:
            return 2
        elif size > 10000:
            return 1
        elif size > 5000:
            return 0
        else:
            return -1

    def is_valid_base64(b64: str) -> bool:
        try:
            base64.b64decode(b64.split(',')[-1], validate=True)
            return True
        except Exception:
            return False

    if not is_valid_base64(photo_base64):
        return "Invalid image data"

    img_format = detect_format(photo_base64)
    quality_score = estimate_quality(len(photo_base64))
    format_score = {"jpeg": 2, "png": 1, "gif": 0, "unknown": -1}.get(img_format, -1)

    total = format_score + quality_score

    if total >= 3:
        return "Looks professional"
    elif total >= 1:
        return "Acceptable"
    else:
        return "Not professional"
    


def mock_photo_check(photo_base64: str) -> str:
    return photo_check_heuristic(photo_base64)




# def mock_photo_check(photo_base64: str) -> str:
#     size = len(photo_base64)
#     format_type = detect_image_format(photo_base64)

#     # Format-based judgment
#     if format_type in ["jpeg", "jpg"]:
#         format_score = 1
#     elif format_type == "png":
#         format_score = 0
#     else:
#         format_score = -1

#     # Size-based quality
#     if size > 30000:
#         quality_score = 2
#     elif size > 10000:
#         quality_score = 1
#     elif size > 5000:
#         quality_score = 0
#     else:
#         quality_score = -1

#     total_score = format_score + quality_score

#     # Fake professional judgment based on total score
#     if total_score >= 2:
#         result = "Looks professional"
#     elif total_score == 1:
#         result = "Decent, could be improved"
#     else:
#         result = "Not professional"

#     # Add a touch of randomness
#     if random.random() < 0.05:
#         result = "Not professional" if result == "Looks professional" else "Looks professional"

#     return result


# def mock_photo_check(photo_base64: str) -> str:
#     size = len(photo_base64)

#     if size > 10000:
#         base_check = "Looks professional"
#     elif size > 5000:
#         base_check = "Decent photo quality"
#     else:
#         base_check = "Poor photo quality"

#     if random.random() < 0.1:
#         base_check = "Not professional" if base_check == "Looks professional" else "Looks professional"

#     return base_check












# import random
# from typing import Tuple

# def mock_score_and_feedback(resume: str, job: str) -> Tuple[int, str]:
#     score = random.randint(40, 95)
#     feedback = f"The resume is a {score}/100 match for this job description."
#     return score, feedback

# def mock_photo_check(photo_base64: str) -> str:
#     return "Looks professional" if random.random() > 0.3 else "Not professional"
