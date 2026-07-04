import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def evaluate_post(text):
    prompt = f"""You are a lead-qualification analyst for a freelance design/development agency.

Below is a post from an online forum. Decide if this is a GENUINE potential client lead
(someone who wants to HIRE a developer/designer for a real project) versus noise
(someone looking for a job themselves, someone promoting their own product, venting, etc).

Respond ONLY with valid JSON, nothing else, in exactly this format:
{{
  "is_genuine_lead": true or false,
  "confidence_score": a number between 0.0 and 1.0,
  "summary": "one sentence describing what they need"
}}

Post:
{text}
"""

    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw_text)
    except:
        result = {"is_genuine_lead": False, "confidence_score": 0.0, "summary": ""}

    return result


if __name__ == "__main__":
    test_post = "I need someone to redesign my company's website, budget is around $3000, please DM me"
    result = evaluate_post(test_post)
    print(result)