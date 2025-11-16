"""Web search functionality for finding senior home care businesses."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import config


class BusinessSearcher:
    """Searches the web for senior home care businesses for sale."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.search_urls = []

    def build_search_urls(self) -> List[str]:
        """Build search URLs for various business listing sites."""
        urls = []

        # BizBuySell - Senior care businesses in California
        urls.append(
            "https://www.bizbuysell.com/businesses-for-sale/"
            "california/los-angeles/?q=senior+care"
        )
        urls.append(
            "https://www.bizbuysell.com/businesses-for-sale/"
            "california/los-angeles/?q=home+care"
        )

        # BizQuest
        urls.append(
            "https://www.bizquest.com/businesses-for-sale/"
            "california/?q=senior+care"
        )

        # Additional generic search that Claude will process
        urls.append(
            "https://www.google.com/search?q=" +
            "senior+home+care+business+for+sale+los+angeles+california"
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
                    'timestamp': time.time()
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
