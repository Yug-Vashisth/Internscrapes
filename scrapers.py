import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time

class InternshipScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
    
    def scrape_all(self) -> List[Dict]:
        """Scrape all companies and return list of internships"""
        all_internships = []
        
        scrapers = [
            self.scrape_nvidia,
            self.scrape_amd,
            self.scrape_google,
            self.scrape_rbc,
            self.scrape_td,
            self.scrape_bmo,
            self.scrape_scotiabank,
            self.scrape_cibc
        ]
        
        for scraper in scrapers:
            try:
                internships = scraper()
                all_internships.extend(internships)
                time.sleep(2)  # Be polite, avoid rate limiting
            except Exception as e:
                print(f"Error in {scraper.__name__}: {e}")
        
        return all_internships
    
    def scrape_nvidia(self) -> List[Dict]:
        """Scrape Nvidia careers page"""
        internships = []
        try:
            # Nvidia uses a careers API
            url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"
            payload = {
                "appliedFacets": {"locationCountry": ["bc33aa3152ec42d4995f4791a106ed09"]},
                "searchText": "intern"
            }
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for job in data.get('jobPostings', [])[:20]:  # Limit to 20 results
                    internships.append({
                        'company': 'Nvidia',
                        'title': job.get('title', 'N/A'),
                        'location': job.get('locationsText', 'N/A'),
                        'url': f"https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite{job.get('externalPath', '')}"
                    })
        except Exception as e:
            print(f"Nvidia scraping error: {e}")
        
        return internships
    
    def scrape_amd(self) -> List[Dict]:
        """Scrape AMD careers page"""
        internships = []
        try:
            url = "https://careers.amd.com/careers-home/jobs?tags3=Intern%2FCo-op"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # AMD's structure varies, this is a generic approach
            job_cards = soup.find_all('a', class_='jobs-list-item')[:20]
            
            for card in job_cards:
                title = card.find('h3')
                location = card.find('span', class_='location')
                
                if title:
                    internships.append({
                        'company': 'AMD',
                        'title': title.get_text(strip=True),
                        'location': location.get_text(strip=True) if location else 'N/A',
                        'url': 'https://careers.amd.com' + card.get('href', '')
                    })
        except Exception as e:
            print(f"AMD scraping error: {e}")
        
        return internships
    
    def scrape_google(self) -> List[Dict]:
        """Scrape Google careers page"""
        internships = []
        try:
            # Google's careers are on a dynamic site, this is a simplified version
            url = "https://www.google.com/about/careers/applications/jobs/results/?q=intern"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            # Note: Google's site is heavily JS-based, may need Selenium for full functionality
            # This is a placeholder structure
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Generic extraction - may need adjustment based on actual structure
            job_elements = soup.find_all('div', class_='gc-card')[:20]
            
            for job in job_elements:
                title_elem = job.find('h2')
                location_elem = job.find('span', class_='gc-job-tags__location')
                link_elem = job.find('a')
                
                if title_elem:
                    internships.append({
                        'company': 'Google',
                        'title': title_elem.get_text(strip=True),
                        'location': location_elem.get_text(strip=True) if location_elem else 'N/A',
                        'url': 'https://www.google.com' + link_elem.get('href', '') if link_elem else url
                    })
        except Exception as e:
            print(f"Google scraping error: {e}")
        
        return internships
    
    def scrape_rbc(self) -> List[Dict]:
        """Scrape RBC careers page"""
        internships = []
        try:
            url = "https://jobs.rbc.com/ca/en/search-results?keywords=intern"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_items = soup.find_all('li', class_='jobs-list-item')[:20]
            
            for item in job_items:
                title_elem = item.find('a', class_='job-title')
                location_elem = item.find('span', class_='job-location')
                
                if title_elem:
                    internships.append({
                        'company': 'RBC',
                        'title': title_elem.get_text(strip=True),
                        'location': location_elem.get_text(strip=True) if location_elem else 'N/A',
                        'url': 'https://jobs.rbc.com' + title_elem.get('href', '')
                    })
        except Exception as e:
            print(f"RBC scraping error: {e}")
        
        return internships
    
    def scrape_td(self) -> List[Dict]:
        """Scrape TD Bank careers page"""
        internships = []
        try:
            url = "https://jobs.td.com/en-CA/search/?searchby=keyword&createNewAlert=false&q=intern"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_results = soup.find_all('tr', class_='data-row')[:20]
            
            for job in job_results:
                title_elem = job.find('a', class_='jobTitle-link')
                location_elem = job.find('span', class_='jobLocation')
                
                if title_elem:
                    internships.append({
                        'company': 'TD Bank',
                        'title': title_elem.get_text(strip=True),
                        'location': location_elem.get_text(strip=True) if location_elem else 'N/A',
                        'url': 'https://jobs.td.com' + title_elem.get('href', '')
                    })
        except Exception as e:
            print(f"TD scraping error: {e}")
        
        return internships
    
    def scrape_bmo(self) -> List[Dict]:
        """Scrape BMO careers page"""
        internships = []
        try:
            url = "https://jobs.bmo.com/ca/en/search-results?keywords=intern"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('li', class_='jobs-list-item')[:20]
            
            for card in job_cards:
                title_elem = card.find('a')
                location_elem = card.find('span', class_='job-location')
                
                if title_elem:
                    internships.append({
                        'company': 'BMO',
                        'title': title_elem.get_text(strip=True),
                        'location': location_elem.get_text(strip=True) if location_elem else 'N/A',
                        'url': 'https://jobs.bmo.com' + title_elem.get('href', '')
                    })
        except Exception as e:
            print(f"BMO scraping error: {e}")
        
        return internships
    
    def scrape_scotiabank(self) -> List[Dict]:
        """Scrape Scotiabank careers page"""
        internships = []
        try:
            url = "https://jobs.scotiabank.com/search/?q=intern"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_rows = soup.find_all('tr', class_='data-row')[:20]
            
            for row in job_rows:
                title_elem = row.find('a', class_='jobTitle')
                location_elem = row.find('span', class_='jobLocation')
                
                if title_elem:
                    internships.append({
                        'company': 'Scotiabank',
                        'title': title_elem.get_text(strip=True),
                        'location': location_elem.get_text(strip=True) if location_elem else 'N/A',
                        'url': 'https://jobs.scotiabank.com' + title_elem.get('href', '')
                    })
        except Exception as e:
            print(f"Scotiabank scraping error: {e}")
        
        return internships
    
    def scrape_cibc(self) -> List[Dict]:
        """Scrape CIBC careers page"""
        internships = []
        try:
            url = "https://cibc.wd3.myworkdayjobs.com/campus"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # CIBC uses Workday, may need API approach similar to Nvidia
            job_links = soup.find_all('a', href=True)[:20]
            
            for link in job_links:
                if 'job' in link.get('href', '').lower():
                    title_text = link.get_text(strip=True)
                    if title_text and len(title_text) > 5:
                        internships.append({
                            'company': 'CIBC',
                            'title': title_text,
                            'location': 'Various',
                            'url': 'https://cibc.wd3.myworkdayjobs.com' + link.get('href', '')
                        })
        except Exception as e:
            print(f"CIBC scraping error: {e}")
        
        return internships
