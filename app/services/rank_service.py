import google.generativeai as genai
from fastapi import UploadFile
from typing import Tuple
import re
import base64
import os
import requests
import fitz  # PyMuPDF
# from docx import Document
# from io import BytesIO
import io
from PIL import Image



from app.config import settings

# Configure Gemini SDK
genai.configure(api_key=settings.GEMINI_API_KEY)

# Initialize the Gemini Vision model
model = genai.GenerativeModel("models/gemini-1.5-flash")


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

# def process_image_for_gemini(image: UploadFile) -> str:
#     try:
#         # Read image bytes
#         image_bytes = image.file.read()
#         pil_image = Image.open(io.BytesIO(image_bytes))

#         # Prepare the image for Gemini API (example prompt, you can adjust it as needed)
#         prompt = "Is this image a professional headshot suitable for a job application?"

#         # Make API call to Gemini Vision
#         url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"

#         headers = {"Content-Type": "application/json"}
#         data = {
#             "contents": [
#                 {"parts": [{"text": prompt}], "media": pil_image}
#             ]
#         }

#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         result = response.json()

#         # Extract the content returned by Gemini Vision
#         model_output = result["candidates"][0]["content"]["parts"][0]["text"]
#         return model_output

#     except Exception as e:
#         return f"Image analysis failed: {str(e)}"


# def process_image_for_gemini(image: UploadFile) -> str:
#     try:
#         # Read image bytes
#         image_bytes = image.file.read()
#         pil_image = Image.open(io.BytesIO(image_bytes))

#         # Convert image to base64
#         buffered = io.BytesIO()
#         pil_image.save(buffered, format="JPEG")
#         img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

#         # Prepare the image for Gemini API (example prompt, you can adjust it as needed)
#         prompt = "Is this image a professional headshot suitable for a job application?"

#         # Make API call to Gemini
#         url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"

#         headers = {"Content-Type": "application/json"}
#         data = {
#             "contents": [
#                 {"parts": [{"text": prompt}], "media": [{"base64": img_str}]}
#             ]
#         }

#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         result = response.json()

#         # Extract the content returned by Gemini
#         model_output = result["candidates"][0]["content"]["parts"][0]["text"]
#         return model_output

#     except Exception as e:
#         return f"Image analysis failed: {str(e)}"

def process_image_for_gemini(image: UploadFile) -> str:
    try:
        # Read image bytes and load with PIL
        image_bytes = image.file.read()
        pil_image = Image.open(io.BytesIO(image_bytes))

        # Prompt to be sent with the image
        prompt = "Is this image a professional headshot suitable for a job application?"

        # Generate content with the Gemini vision model
        response = model.generate_content([prompt, pil_image], stream=False)
        response.resolve()

        return response.text

    except Exception as e:
        return f"Image analysis failed: {str(e)}"  

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
    
def process_image_from_analysis(image_file: UploadFile):
    try:
        contents = image_file.file.read()
        image = Image.open(BytesIO(contents))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # 👇 Pass img_str to Gemini here if needed
        # For now just return a dummy check
        return "Valid photo detected and processed"

    except Exception as e:
        return f"Invalid image data: {str(e)}"


def mock_photo_check(photo_base64: str) -> str:
    return photo_check_heuristic(photo_base64)

async def extract_text_from_resume(file: UploadFile) -> str:
    # Read the file content into memory
    file_content = await file.read()
    file_extension = file.filename.split('.')[-1].lower()

    # Extract text based on file type
    if file_extension == "pdf":
        return extract_text_from_pdf(file_content)
    elif file_extension == "docx":
        return extract_text_from_docx(file_content)
    else:
        raise ValueError("Unsupported file type")

def extract_text_from_pdf(file_content: bytes) -> str:
    # Using PyMuPDF to extract text from a PDF
    doc = fitz.open(stream=file_content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

def extract_text_from_docx(file_content: bytes) -> str:
    # Using python-docx to extract text from a DOCX file
    doc = Document(BytesIO(file_content))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text




