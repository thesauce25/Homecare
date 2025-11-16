"""Claude AI integration for analyzing business listings."""
from anthropic import Anthropic
from typing import List, Dict, Optional
import json
import config
from bs4 import BeautifulSoup


class ClaudeAnalyzer:
    """Uses Claude AI to extract structured business information from web content."""

    def __init__(self):
        config.validate_config()
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)

    def clean_html(self, html: str, max_length: int = 100000) -> str:
        """Clean and truncate HTML to extract readable text."""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Break into lines and remove leading/trailing space
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length] + "... [truncated]"

        return text

    def extract_business_listings(self, page_content: str, source_url: str) -> List[Dict]:
        """
        Use Claude to identify and extract business listings from a page.
        Returns a list of business listing URLs found on the page.
        """
        cleaned_text = self.clean_html(page_content)

        prompt = f"""Analyze this web page content and identify any senior home care or home health care
business listings that are for sale in Los Angeles or Southern California.

For each business listing you find, extract the URL/link to the full listing details.

Page URL: {source_url}

Page Content:
{cleaned_text[:50000]}

Return ONLY a JSON array of listing URLs found, like this:
["url1", "url2", "url3"]

If no listings are found, return an empty array: []
"""

        try:
            message = self.client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # Extract JSON from response
            if response_text.startswith('['):
                urls = json.loads(response_text)
                return urls if isinstance(urls, list) else []
            else:
                return []

        except Exception as e:
            print(f"Error extracting listings with Claude: {e}")
            return []

    def analyze_business_listing(self, page_content: str, listing_url: str) -> Optional[Dict]:
        """
        Use Claude to extract detailed business information from a listing page.
        Returns a dictionary with business details or None if no valid business found.
        """
        cleaned_text = self.clean_html(page_content)

        prompt = f"""Analyze this senior home care business listing and extract structured information.

Focus on extracting:
1. Business Name
2. Financial Information (asking price, revenue, EBITDA, cash flow, etc.)
3. Broker Information (broker name, company, phone, email)
4. Any additional relevant details

Listing URL: {listing_url}

Page Content:
{cleaned_text[:80000]}

Return the information in this exact JSON format:
{{
    "business_name": "Name of the business",
    "financial_info": "Asking Price: $X, Annual Revenue: $Y, EBITDA: $Z, etc.",
    "broker_info": "Broker Name, Company, Phone: XXX-XXX-XXXX, Email: xxx",
    "additional_notes": "Any other relevant details about location, size, years in business, etc."
}}

If this is not a senior/home care business listing in Los Angeles/Southern California, return: {{"skip": true}}
"""

        try:
            message = self.client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # Find JSON in response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                business_data = json.loads(json_str)

                # Check if we should skip this listing
                if business_data.get('skip'):
                    return None

                # Add the listing URL
                business_data['listing_link'] = listing_url

                return business_data
            else:
                print(f"Could not parse JSON from Claude response for {listing_url}")
                return None

        except Exception as e:
            print(f"Error analyzing business with Claude: {e}")
            return None

    def analyze_search_results(self, search_results: List[Dict]) -> List[Dict]:
        """
        Analyze search results to find and extract business listings.
        Returns a list of business dictionaries with extracted information.
        """
        all_businesses = []
        all_listing_urls = set()

        # Check if we have direct listings or search pages
        direct_listings = [r for r in search_results if r.get('is_direct_listing', False)]
        search_pages = [r for r in search_results if not r.get('is_direct_listing', False)]

        # Handle direct listings (from manual_urls.txt)
        if direct_listings:
            print("\n=== Analyzing Direct Business Listings ===")

            for idx, result in enumerate(direct_listings, 1):
                url = result['url']
                print(f"\n[{idx}/{len(direct_listings)}] Analyzing: {url}")

                business_data = self.analyze_business_listing(result['content'], url)

                if business_data:
                    print(f"  ✓ Extracted: {business_data.get('business_name', 'Unknown')}")
                    all_businesses.append(business_data)
                else:
                    print(f"  ✗ Skipped (not relevant or parsing failed)")

        # Handle search pages (automated search)
        if search_pages:
            print("\n=== Phase 1: Finding Business Listings ===")

            # First, extract listing URLs from search pages
            for result in search_pages:
                print(f"\nScanning: {result['url']}")
                listing_urls = self.extract_business_listings(
                    result['content'],
                    result['url']
                )
                print(f"  Found {len(listing_urls)} potential listings")
                all_listing_urls.update(listing_urls)

            print(f"\n=== Phase 2: Analyzing {len(all_listing_urls)} Business Listings ===")

            # Now analyze each individual listing
            for idx, url in enumerate(list(all_listing_urls)[:config.MAX_SEARCH_RESULTS], 1):
                print(f"\n[{idx}/{min(len(all_listing_urls), config.MAX_SEARCH_RESULTS)}] Analyzing: {url}")

                # Fetch the listing page
                from search_engine import BusinessSearcher
                searcher = BusinessSearcher()
                html = searcher.fetch_page(url)

                if html:
                    business_data = self.analyze_business_listing(html, url)

                    if business_data:
                        print(f"  ✓ Extracted: {business_data.get('business_name', 'Unknown')}")
                        all_businesses.append(business_data)
                    else:
                        print(f"  ✗ Skipped (not relevant or parsing failed)")

        return all_businesses
