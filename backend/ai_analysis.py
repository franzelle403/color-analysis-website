import os
import base64
import requests
import json
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def analyze_image_with_ai(image_data: bytes, content_type: str):

    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is not configured."
        )

    # Convert the image into base64
    base64_image = base64.b64encode(image_data).decode("utf-8")

    # Create a data URL for the image
    image_url = f"data:{content_type};base64,{base64_image}"

    prompt = """
You are a cosmetic color-analysis assistant.

Analyze the visible facial skin in the uploaded image.

Your job is to estimate characteristics useful for cosmetic
shade matching.

Return ONLY valid JSON.

Use exactly these fields:

{
    "skin_depth": "",
    "undertone": "",
    "contrast": "",
    "lighting": "",
    "image_quality": "",
    "confidence": 0
}

Allowed values:

skin_depth:
- very_fair
- fair
- light
- medium
- tan
- deep
- uncertain

undertone:
- cool
- neutral
- warm
- olive
- uncertain

contrast:
- low
- medium
- high
- uncertain

lighting:
- good
- acceptable
- poor

image_quality:
- suitable
- unsuitable

confidence:
- number from 0 to 1

Important:

Do not infer race, ethnicity, nationality, health conditions,
age, or other personal characteristics.

Focus only on visible color characteristics relevant to
cosmetic shade matching.

If lighting or image quality makes the analysis unreliable,
use "uncertain" where appropriate and reduce confidence.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },

        json={
            "model": "openrouter/free",

            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],

            "temperature": 0.1
        },

        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    ai_text = result["choices"][0]["message"]["content"]

    # Remove markdown code fences if the model adds them
    ai_text = ai_text.replace("```json", "").replace("```", "").strip()

    # Convert the AI response from text into Python JSON
    analysis = json.loads(ai_text)

    return analysis