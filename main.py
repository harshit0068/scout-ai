import time
from scraper import run_scan_cycle as scan_hackernews
from remoteok_scraper import scan_remoteok

def run_all_sources():
    print("\n========== Starting full scan cycle ==========")
    
    scan_hackernews()
    scan_remoteok()
    
    print("========== Full scan cycle complete ==========\n")


if __name__ == "__main__":
    while True:
        run_all_sources()
        print("Sleeping for 15 minutes before next full cycle...")
        time.sleep(14400)