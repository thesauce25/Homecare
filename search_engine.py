"""Web search functionality for finding senior home care businesses."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import os
import config


class BusinessSearcher:
    """Searches the web for senior home care businesses for sale."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.search_urls = []

    def load_manual_urls(self) -> List[str]:
        """Load manually specified URLs from manual_urls.txt file."""
        urls = []
        manual_file = "manual_urls.txt"

        if os.path.exists(manual_file):
            try:
                with open(manual_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            if line.startswith('http'):
                                urls.append(line)
            except Exception as e:
                print(f"Error reading manual URLs: {e}")

        return urls

    def build_search_urls(self) -> List[str]:
        """Build search URLs for various business listing sites."""
        urls = []

        # Updated URLs based on working business listing sites
        # BizBuySell - Los Angeles County home health care businesses
        urls.append(
            "https://www.bizbuysell.com/california/los-angeles-county/"
            "home-health-care-businesses-for-sale/"
        )

        # LoopNet - Los Angeles home health care businesses
        urls.append(
            "https://www.loopnet.com/biz/california/los-angeles-county/"
            "home-health-care-businesses-for-sale/"
        )

        # BizQuest - California home health care
        urls.append(
            "https://www.bizquest.com/home-health-care-businesses-for-sale-in-california/"
        )

        # DealStream - California home health care
        urls.append(
            "https://dealstream.com/california/home-health-care-businesses-for-sale"
        )

        return urls

    def fetch_page(self, url: str) -> str:
        """Fetch HTML content from a URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def extract_links_from_html(self, html: str, base_domain: str = None) -> List[str]:
        """Extract relevant business listing links from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []

        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']

            # Filter for business listing URLs
            if any(domain in href for domain in config.SEARCH_SOURCES):
                if href.startswith('http'):
                    links.append(href)

        return list(set(links))  # Remove duplicates

    def search_for_businesses(self) -> List[Dict[str, str]]:
        """
        Perform web searches and return raw HTML content for Claude to analyze.
        Returns a list of dictionaries with 'url' and 'content'.
        """
        # First, check for manual URLs
        manual_urls = self.load_manual_urls()

        if manual_urls:
            print(f"Found {len(manual_urls)} manually specified URLs in manual_urls.txt")
            print("Using manual URLs instead of automated search...")
            results = []

            for url in manual_urls:
                print(f"  Fetching manual URL: {url}")
                html_content = self.fetch_page(url)

                if html_content:
                    results.append({
                        'url': url,
                        'content': html_content,
                        'timestamp': time.time(),
                        'is_direct_listing': True  # These are direct listings, not search pages
                    })

                time.sleep(1)

            print(f"Retrieved {len(results)} manual listings")
            return results

        # Otherwise, use automated search
        search_urls = self.build_search_urls()
        results = []

        print(f"Searching {len(search_urls)} sources for senior care businesses...")

        for url in search_urls:
            print(f"  Fetching: {url}")
            html_content = self.fetch_page(url)

            if html_content:
                results.append({
                    'url': url,
                    'content': html_content,
                    'timestamp': time.time(),
                    'is_direct_listing': False  # These are search pages
                })

            # Be respectful with rate limiting
            time.sleep(2)

        print(f"Retrieved {len(results)} pages for analysis")
        return results

    def get_specific_listing_pages(self, listing_urls: List[str]) -> List[Dict[str, str]]:
        """Fetch specific business listing pages for detailed analysis."""
        results = []

        for url in listing_urls[:config.MAX_SEARCH_RESULTS]:
            print(f"  Fetching listing: {url}")
            html_content = self.fetch_page(url)

            if html_content:
                results.append({
                    'url': url,
                    'content': html_content
                })

            time.sleep(1)  # Rate limiting

        return results
