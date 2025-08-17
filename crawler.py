"""
crawler.py - Efficient & Ethical WebWanderer Crawler (robots.txt + content-type filtering)
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib import robotparser
from supabase import create_client, Client
import datetime
import os
import time

# Curated seed URLs for Python and JavaScript project ideas/resources
seed_urls = [
    'https://github.com/topics/project-showcase',
    'https://www.dataquest.io/blog/python-projects-for-beginners/',
    'https://realpython.com/tutorials/projects/',
    'https://www.geeksforgeeks.org/python/python-projects-beginner-to-advanced/',
    'https://data-flair.training/blogs/python-project-ideas/',
    'https://www.guvi.in/blog/best-javascript-project-ideas/',
    'https://dev.to/bpk45_0670a02e0f3a6839b3a/top-10-websites-for-frontend-design-inspiration-and-animations-k26',
    'https://www.reddit.com/r/learnpython/',
    'https://www.reddit.com/r/learnjavascript/',
    'https://frontendmentor.io/',
    'https://codepen.io/trending',
    'https://codrops.com/playground/',
    'https://www.awwwards.com/websites/'
]

CRAWL_LIMIT = 200
USER_AGENT = 'WebWandererBot/1.0'

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_page_data(url):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title Found'
        content = soup.get_text(separator=' ', strip=True)
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            abs_url = urljoin(url, href)
            if abs_url.startswith('http'):
                links.add(abs_url)
        return title, content, links
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None, set()

if __name__ == "__main__":
    queue = list(seed_urls)
    visited = set()
    count = 0
    while queue and count < CRAWL_LIMIT:
        current_url = queue.pop(0)
        if current_url in visited:
            continue
        # robots.txt check
        parsed = urlparse(current_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = robotparser.RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
        except Exception as e:
            print(f"Could not read robots.txt for {robots_url}: {e}")
        if not rp.can_fetch(USER_AGENT, current_url):
            print(f"DISALLOWED: Skipping {current_url} due to robots.txt")
            visited.add(current_url)
            continue
        # Content-Type check with HEAD request
        try:
            head_resp = requests.head(current_url, timeout=5, allow_redirects=True, headers={"User-Agent": USER_AGENT})
            content_type = head_resp.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                print(f"SKIPPING: {current_url} is not an HTML page (Content-Type: {content_type})")
                visited.add(current_url)
                continue
        except Exception as e:
            print(f"SKIPPING: {current_url} due to HEAD request error: {e}")
            visited.add(current_url)
            continue
        print(f"ALLOWED: Crawling ({count+1}/{CRAWL_LIMIT}): {current_url}")
        time.sleep(1)  # Politeness delay
        title, content, links = fetch_page_data(current_url)
        if title and content:
            data = {
                "url": current_url,
                "title": title,
                "content": content,
                "crawled_at": datetime.datetime.utcnow().isoformat()
            }
            try:
                result = supabase.table("pages").insert(data).execute()
                if hasattr(result, 'status_code') and result.status_code == 201:
                    print("Indexed successfully.")
                else:
                    print("Failed to index page.", result)
            except Exception as e:
                print(f"Supabase error: {e}")
            count += 1
        visited.add(current_url)
        for link in links:
            if link not in visited and link not in queue:
                queue.append(link)
    print(f"Crawling finished. Indexed {count} pages.")
