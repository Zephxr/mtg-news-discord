import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
BASE_URL = "https://magic.wizards.com/en/news/archive"
LAST_ARTICLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_article.txt")

def get_latest_article():
    try:
        logger.info(f"Fetching articles from {BASE_URL}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(BASE_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        article = soup.find('div', class_='css-Nm7vm')
        if not article:
            logger.warning("No articles found with class 'css-Nm7vm'")
            return None
            
        title = article.find('h3')
        if title:
            title = title.text.strip()
        else:
            logger.warning("No title found in article")
            return None
            
        article_content = article.find('article', class_='css-415ug')
        if not article_content:
            logger.warning("No article content found")
            return None
            
        content_div = article_content.find('div', class_='css-3qxBv')
        if not content_div:
            logger.warning("No content div found")
            return None
            
        link = content_div.find('a', attrs={'data-navigation-type': 'client-side'})
        if link:
            link = link['href']
            if not link.startswith('http'):
                link = f"https://magic.wizards.com{link}"
        else:
            logger.warning("No link found for article")
            return None
            
        logger.info(f"Found article: {title}")
        logger.info(f"Article URL: {link}")
        return {
            'title': title,
            'url': link
        }
    except Exception as e:
        logger.error(f"Error fetching articles: {e}")
        return None

def load_last_article():
    try:
        with open(LAST_ARTICLE_FILE, 'r') as f:
            last_url = f.read().strip()
            logger.info(f"Last article URL: {last_url}")
            return last_url
    except FileNotFoundError:
        logger.info("No last article file found")
        return None

def save_last_article(url):
    with open(LAST_ARTICLE_FILE, 'w') as f:
        f.write(url)
        logger.info(f"Saved new last article URL: {url}")

def send_webhook(article):
    if not WEBHOOK_URL:
        logger.error("Webhook URL not configured")
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
        logger.info(f"Sending webhook for article: {article['title']}")
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        logger.info("Webhook sent successfully")
    except Exception as e:
        logger.error(f"Error sending webhook: {e}")

logger.info("Starting MTG Article Bot check")
last_article_url = load_last_article()
latest_article = get_latest_article()

if latest_article:
    if latest_article['url'] != last_article_url:
        logger.info("New article detected")
        send_webhook(latest_article)
        save_last_article(latest_article['url'])
    else:
        logger.info("No new articles found")
else:
    logger.warning("Could not fetch latest article") 