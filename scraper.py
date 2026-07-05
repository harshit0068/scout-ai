import requests
import time
from db import insert_lead
from ai_evaluator import evaluate_post

keywords = [
    "hiring",
    "looking for a developer",
    "freelance",
    "need a designer",
    "looking for a designer",
    "need a developer",
    "seeking a",
    "who wants to work",
    "co-founder",
    "contractor"
]

SOURCE_NAME = "Hacker News"

def run_scan_cycle():
    print(f"\n--- Scanning {SOURCE_NAME} ---")

    response = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")
    story_ids = response.json()

    genuine_count = 0

    for story_id in story_ids[:100]:
        post_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
        post_data = post_response.json()

        title = post_data.get("title", "")
        text = post_data.get("text", "")
        full_text = (title + " " + text).lower()

        for keyword in keywords:
            if keyword in full_text:
                author = post_data.get("by", "unknown")
                url = f"https://news.ycombinator.com/item?id={post_data.get('id')}"
                combined_text = title + " " + text

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

                time.sleep(13)
                break

    print(f"--- {SOURCE_NAME} cycle complete: {genuine_count} genuine leads found ---\n")


if __name__ == "__main__":
    while True:
        run_scan_cycle()
        print("Sleeping for 5 minutes...")
        time.sleep(300)