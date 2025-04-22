import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json

load_dotenv()

# Configuration
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
CHECK_INTERVAL = 300
BASE_URL = "https://magic.wizards.com/en/news/archive"
LAST_ARTICLE_FILE = "last_article.txt"

def get_latest_article():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        article = soup.find('div', class_='article-item')
        if not article:
            return None
            
        title = article.find('h3').text.strip()
        link = article.find('a')['href']
        if not link.startswith('http'):
            link = f"https://magic.wizards.com{link}"
            
        return {
            'title': title,
            'url': link
        }
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return None

def load_last_article():
    try:
        with open(LAST_ARTICLE_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_article(url):
    with open(LAST_ARTICLE_FILE, 'w') as f:
        f.write(url)

def send_webhook(article):
    if not WEBHOOK_URL:
        print("Error: Webhook URL not configured")
        return
        
    payload = {
        "embeds": [{
            "title": article['title'],
            "url": article['url'],
            "color": 0x000000,
            "footer": {
                "text": "Magic: The Gathering"
            }
        }]
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending webhook: {e}")

def main():
    print("MTG Article Bot started...")
    
    last_article_url = load_last_article()
    
    while True:
        try:
            latest_article = get_latest_article()
            
            if latest_article and latest_article['url'] != last_article_url:
                print(f"New article found: {latest_article['title']}")
                send_webhook(latest_article)
                save_last_article(latest_article['url'])
                last_article_url = latest_article['url']
            
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main() 