#!/usr/bin/env python3
"""
Internship Scraper - Main Script
Scrapes internship opportunities and sends daily email digest
"""

import os
from dotenv import load_dotenv
from database import InternshipDB
from scrapers import InternshipScraper
from email_sender import EmailSender

def main():
    """Main function to run the scraper"""
    print("Starting internship scraper...")
    
    # Load environment variables
    load_dotenv('lebron.env')
    
    # Get configuration from environment
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    
    if not all([sender_email, sender_password, recipient_email]):
        print("ERROR: Missing required environment variables.")
        print("Please set SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL in .env file")
        return
    
    # Initialize components
    db = InternshipDB()
    scraper = InternshipScraper()
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    
    # Scrape all companies
    print("Scraping internship opportunities...")
    all_internships = scraper.scrape_all()
    print(f"Found {len(all_internships)} total internship postings")
    
    # Process and identify new internships
    new_internships = []
    for internship in all_internships:
        is_new = db.add_internship(
            company=internship['company'],
            title=internship['title'],
            location=internship['location'],
            url=internship['url']
        )
        if is_new:
            new_internships.append(internship)
    
    print(f"Identified {len(new_internships)} new internship(s)")
    
    # Send email digest
    print("Sending email digest...")
    email_sender.send_daily_digest(recipient_email, new_internships)
    
    print("Done!")

if __name__ == "__main__":
    main()
