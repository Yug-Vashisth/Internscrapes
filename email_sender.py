import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime

class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_daily_digest(self, recipient_email: str, internships: List[Dict]):
        """Send daily email digest of new internships"""
        subject = f"Internship Digest - {datetime.now().strftime('%B %d, %Y')}"
        
        if not internships:
            body = self._create_no_opportunities_email()
        else:
            body = self._create_opportunities_email(internships)
        
        self._send_email(recipient_email, subject, body)
    
    def _create_opportunities_email(self, internships: List[Dict]) -> str:
        """Create HTML email body with new opportunities"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
                .job {{ 
                    background-color: #f8f9fa; 
                    padding: 15px; 
                    margin: 10px 0; 
                    border-left: 4px solid #3498db;
                    border-radius: 4px;
                }}
                .job-title {{ font-weight: bold; font-size: 16px; color: #2c3e50; }}
                .job-location {{ color: #7f8c8d; font-style: italic; }}
                .job-link {{ color: #3498db; text-decoration: none; }}
                .job-link:hover {{ text-decoration: underline; }}
                .summary {{ background-color: #e8f4f8; padding: 10px; border-radius: 4px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>🎯 New Internship Opportunities</h1>
            <div class="summary">
                <strong>{len(internships)} new internship{'' if len(internships) == 1 else 's'} found today!</strong>
            </div>
        """
        
        # Group by company
        companies = {}
        for internship in internships:
            company = internship['company']
            if company not in companies:
                companies[company] = []
            companies[company].append(internship)
        
        # Add jobs grouped by company
        for company, jobs in sorted(companies.items()):
            html += f"<h2>{company} ({len(jobs)} opening{'s' if len(jobs) > 1 else ''})</h2>"
            
            for job in jobs:
                html += f"""
                <div class="job">
                    <div class="job-title">{job['title']}</div>
                    <div class="job-location">📍 {job['location']}</div>
                    <div><a href="{job['url']}" class="job-link">Apply Here →</a></div>
                </div>
                """
        
        html += """
            <hr style="margin-top: 30px; border: none; border-top: 1px solid #ddd;">
            <p style="color: #7f8c8d; font-size: 12px;">
                This is an automated email from your Internship Scraper. 
                Good luck with your applications! 🚀
            </p>
        </body>
        </html>
        """
        
        return html
    
    def _create_no_opportunities_email(self) -> str:
        """Create email body when no new opportunities are found"""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .message { 
                    background-color: #f8f9fa; 
                    padding: 20px; 
                    border-left: 4px solid #95a5a6;
                    border-radius: 4px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div class="message">
                <h2>📭 No New Internships Today</h2>
                <p>No new internship opportunities were found today across the monitored companies.</p>
                <p>Keep checking back - new opportunities are posted regularly!</p>
            </div>
            <hr style="margin-top: 30px; border: none; border-top: 1px solid #ddd;">
            <p style="color: #7f8c8d; font-size: 12px;">
                This is an automated email from your Internship Scraper.
            </p>
        </body>
        </html>
        """
        return html
    
    def _send_email(self, recipient: str, subject: str, html_body: str):
        """Send the email via SMTP"""
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                print(f"Email sent successfully to {recipient}")
        except Exception as e:
            print(f"Failed to send email: {e}")
