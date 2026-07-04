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

def run_scan_cycle():
    print("\n--- Starting new scan cycle ---")

    response = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")
    story_ids = response.json()

    matches = []

    for story_id in story_ids[:100]:
        post_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
        post_data = post_response.json()

        title = post_data.get("title", "")
        text = post_data.get("text", "")
        full_text = (title + " " + text).lower()

        for keyword in keywords:
            if keyword in full_text:
                clean_post = {
                    "author": post_data.get("by"),
                    "url": f"https://news.ycombinator.com/item?id={post_data.get('id')}",
                    "text": title + " " + text
                }

                ai_result = evaluate_post(clean_post["text"])
                print(f"AI verdict: {ai_result}")

                if ai_result["is_genuine_lead"]:
                    insert_lead(clean_post["author"], clean_post["url"], clean_post["text"])
                    matches.append(clean_post)

                break

    print(f"--- Cycle complete: {len(matches)} genuine leads found ---\n")


if __name__ == "__main__":
    while True:
        run_scan_cycle()
        print("Sleeping for 5 minutes...")
        time.sleep(300)  # 300 seconds = 5 minutes