# 🎯 Internship Opportunity Scraper

An automated web scraper that monitors internship opportunities from major tech companies and Canadian banks, sending you a daily email digest of new postings.


**Tech Companies:**
- Nvidia
- AMD
- Google

**Canadian Banks:**
- RBC (Royal Bank of Canada)
- TD Bank
- BMO (Bank of Montreal)
- Scotiabank
- CIBC

## ✨ Features

- Scrapes multiple company career pages daily
- Tracks previously seen postings to identify new opportunities
-  Sends formatted HTML email digests every morning
- SQLite database for persistent storage
- Clean, organized email format grouped by company
- Sends notification even when no new postings are found


### 1. Install Dependencies

```bash
cd ~/internship_scraper
pip3 install -r requirements.txt
```

### 2. Configure Email Settings

Copy the example environment file and edit it with your credentials:

```bash
cp .env.example .env
nano .env  # or use your preferred text editor
```

**For Gmail users:**
1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Generate a new app password

**Example `.env` file:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=youremail@gmail.com
SENDER_PASSWORD=your_app_password_here
RECIPIENT_EMAIL=youremail@gmail.com
```

## Schedule Daily Emails

### Option 1: Using the Python Scheduler (Recommended)

Run the scheduler script, which will keep running and execute the scraper daily at 8:00 AM:

```bash
python3 scheduler.py
```

To run it in the background:

```bash
nohup python3 scheduler.py > scraper.log 2>&1 &
```

To change the time, edit `scheduler.py` line 19:
```python
schedule.every().day.at("08:00").do(job)  # Change "08:00" to your preferred time
```


Load the job:

```bash
launchctl load ~/Library/LaunchAgents/com.internshipscraper.daily.plist
```

## 📁 Project Structure

```
internship_scraper/
├── main.py              # Main orchestration script
├── scheduler.py         # Daily scheduler using Python schedule library
├── scrapers.py          # Web scraping logic for all companies
├── database.py          # SQLite database management
├── email_sender.py      # Email formatting and sending
├── requirements.txt     # Python dependencies
├── .env                 # Your email configuration (not in git)
├── .env.example         # Template for environment variables
├── internships.db       # SQLite database (auto-created)
└── README.md           # This file
```

##  License

This is a personal project.