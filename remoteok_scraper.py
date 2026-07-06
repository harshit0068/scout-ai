import requests
import time
from ai_evaluator import evaluate_post
from db import insert_lead

SOURCE_NAME = "RemoteOK"

def scan_remoteok():
    print(f"\n--- Scanning {SOURCE_NAME} ---")

    response = requests.get(
        "https://remoteok.com/api",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    jobs = response.json()
    jobs = jobs[1:]  # first item is just metadata

    freelance_signals = [
        "freelance", "freelancer", "agency", "hire a developer",
        "hire a designer", "looking for a contractor",
        "project basis", "short-term project", "one-off project"
    ]

    genuine_count = 0

    for job in jobs:
        position = job.get("position", "")
        description = job.get("description", "")
        full_text = (position + " " + description).lower()

        is_relevant = any(signal in full_text for signal in freelance_signals)

        if is_relevant:
            author = job.get("company", "unknown")
            url = job.get("url", job.get("apply_url", ""))
            combined_text = position + " " + description

            try:
                ai_result = evaluate_post(combined_text)
                print(f"AI verdict: {ai_result}")

                insert_lead(
                    source=SOURCE_NAME,
                    author=author,
                    url=url,
                    text=combined_text,
                    is_genuine=ai_result["is_genuine_lead"],
                    confidence_score=ai_result["confidence_score"],
                    summary=ai_result["summary"]
                )

                if ai_result["is_genuine_lead"]:
                    genuine_count += 1

            except Exception as e:
                print(f"AI call failed, skipping this post: {e}")

            time.sleep(2)

    print(f"--- {SOURCE_NAME} cycle complete: {genuine_count} genuine leads found ---\n")


if __name__ == "__main__":
    scan_remoteok()