#!/usr/bin/env python3
"""
Scheduler script to run the scraper daily at a specified time
"""

import schedule
import time
from main import main

def job():
    """Job to be scheduled"""
    print(f"\n{'='*50}")
    print(f"Running scheduled job at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    main()

if __name__ == "__main__":
    # Schedule the job to run every day at 8:00 AM
    schedule.every().day.at("08:00").do(job)
    
    print("Internship Scraper Scheduler Started")
    print("Will run daily at 8:00 AM")
    print("Press Ctrl+C to stop\n")
    
    # Run once immediately on startup (optional - comment out if not desired)
    print("Running initial scan...")
    job()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
