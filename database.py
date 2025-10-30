import sqlite3
from datetime import datetime
from typing import List, Dict

class InternshipDB:
    def __init__(self, db_path='internships.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS internships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                title TEXT NOT NULL,
                location TEXT,
                url TEXT NOT NULL UNIQUE,
                first_seen DATE NOT NULL,
                last_seen DATE NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_internship(self, company: str, title: str, location: str, url: str) -> bool:
        """
        Add a new internship to the database.
        Returns True if it's a new posting, False if it already exists.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        today = datetime.now().date().isoformat()
        
        try:
            cursor.execute('''
                INSERT INTO internships (company, title, location, url, first_seen, last_seen)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (company, title, location, url, today, today))
            conn.commit()
            conn.close()
            return True  # New internship
        except sqlite3.IntegrityError:
            # Already exists, update last_seen
            cursor.execute('''
                UPDATE internships
                SET last_seen = ?
                WHERE url = ?
            ''', (today, url))
            conn.commit()
            conn.close()
            return False  # Existing internship
    
    def get_new_internships_today(self) -> List[Dict]:
        """Get all internships that were first seen today"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        today = datetime.now().date().isoformat()
        
        cursor.execute('''
            SELECT company, title, location, url
            FROM internships
            WHERE first_seen = ?
            ORDER BY company, title
        ''', (today,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'company': row[0],
                'title': row[1],
                'location': row[2],
                'url': row[3]
            }
            for row in results
        ]
