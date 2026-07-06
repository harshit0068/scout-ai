import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        raw_text = response.choices[0].message.content.strip()
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw_text)
    except Exception as e:
        print(f"[ai_evaluator] classification failed, defaulting to non-lead: {e}")
        result = {"is_genuine_lead": False, "confidence_score": 0.0, "summary": ""}

    return result


if __name__ == "__main__":
    test_post = "I need someone to redesign my company's website, budget is around $3000, please DM me"
    result = evaluate_post(test_post)
    print(result)