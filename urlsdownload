import requests
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET
import csv
import os
import time
from urllib.parse import urlparse, urlunparse

def get_channel_id(youtube_url):
    """Extract channelId from YouTube channel page source."""
    clean_url = youtube_url.replace('view-source:', '')
    print(f"Fetching data from: {clean_url}")

    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(clean_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        channel_id = None
        meta_tag = soup.find('meta', property='og:url')
        if meta_tag and 'content' in meta_tag.attrs:
            url_content = meta_tag['content']
            if '/channel/' in url_content:
                print(url_content)
                channel_id = url_content.split('/channel/')[1].split('?')[0]
        if not channel_id:
            link_tag = soup.find('link', rel='canonical')
            if link_tag and 'href' in link_tag.attrs:
                url_content = link_tag['href']
                if '/channel/' in url_content:
                    channel_id = url_content.split('/channel/')[1].split('?')[0]

        if channel_id:
            print(f"✅ Found channelId: {channel_id}")
            return channel_id
        else:
            print("❌ channelId not found.")
            return None

    except Exception as e:
        print(f"❌ Error extracting channelId: {e}")
        return None

def fetch_rss(channel_id, csv_file='media_urls.csv'):
    """Fetch media:content URLs from YouTube RSS feed and save unique ones."""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(rss_url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Failed to fetch RSS feed: {response.status_code}")
            return

        root = ET.fromstring(response.content)

        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'media': 'http://search.yahoo.com/mrss/',
            'yt': 'http://www.youtube.com/xml/schemas/2015'
        }

        existing_urls = set()
        if os.path.exists(csv_file):
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    existing_urls.add(row[0]) 
        new_urls = []

        for entry in root.findall('atom:entry', ns):
            media_content = entry.find('media:group/media:content', ns)
            if media_content is not None:
                url = media_content.attrib.get('url')
                if url and url not in existing_urls:
                    new_urls.append([url])
                    existing_urls.add(url)

        # Save new URLs
        if new_urls:
            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(new_urls)
            print(f"✅ Added {len(new_urls)} new media URLs to '{csv_file}'")
        else:
            print("🔁 No new media URLs found.")

    except Exception as e:
        print(f"❌ Error fetching or parsing RSS: {e}")

def start_watching(youtube_url, interval=10):
    """Continuously check for new media content URLs every X seconds."""
    channel_id = get_channel_id(youtube_url)
    if not channel_id:
        print("❌ Exiting. Cannot fetch channel ID.")
        return

    print(f"🔍 Watching for new media content every {interval} seconds...\n")
    while True:
        fetch_rss(channel_id)
        time.sleep(interval)

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/@neeteshjkunwar"  
