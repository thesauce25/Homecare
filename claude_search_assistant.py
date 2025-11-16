#!/usr/bin/env python3
"""
Claude Search Assistant
A helper script to use Claude Code's web search for finding business listings.
This avoids bot detection by leveraging Claude's native web search.
"""

def print_search_queries():
    """Print search queries for the user to run through Claude Code."""
    queries = [
        "Find senior home care businesses for sale in Los Angeles on bizbuysell.com - provide direct URLs to listings",
        "Find home health care businesses for sale in California on bizquest.com - provide direct URLs to listings",
        "Find senior care businesses for sale in Los Angeles County on loopnet.com - provide direct URLs to listings",
        "Find home care businesses for sale in Southern California on businessbroker.net - provide direct URLs to listings"
    ]

    print("=" * 70)
    print(" Claude Search Assistant ".center(70, "="))
    print("=" * 70)
    print("\nThis tool helps you use Claude Code's web search to find business")
    print("listings without triggering bot detection.")
    print("\nINSTRUCTIONS:")
    print("-" * 70)
    print("1. Copy each search query below")
    print("2. Paste it into Claude Code (the AI you're talking to)")
    print("3. Claude will search the web and find business listing URLs")
    print("4. Copy all the URLs Claude finds")
    print("5. Paste them into 'manual_urls.txt' (one URL per line)")
    print("6. Run 'python main.py' to analyze the businesses")
    print("=" * 70)

    print("\n📋 SEARCH QUERIES TO RUN:\n")
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")
        print()

    print("=" * 70)
    print("\nAfter Claude finds URLs, paste them into 'manual_urls.txt'")
    print("Then run: python main.py")
    print("=" * 70)


def create_template_file():
    """Create a template manual_urls.txt file."""
    template = """# Manual URLs for Senior Care Businesses
# Add one URL per line (lines starting with # are ignored)
#
# Example URLs:
# https://www.bizbuysell.com/Business-Opportunity/specific-listing-123/
# https://www.bizquest.com/businesses-for-sale/listing/12345.html
#
# Instructions:
# 1. Run: python claude_search_assistant.py
# 2. Use Claude Code to search for businesses (avoids bot detection)
# 3. Paste the URLs Claude finds below (remove the # to uncomment)
# 4. Save this file
# 5. Run: python main.py

"""

    try:
        with open('manual_urls.txt', 'w') as f:
            f.write(template)
        print("\n✓ Created manual_urls.txt template file")
    except Exception as e:
        print(f"\n❌ Error creating template: {e}")


if __name__ == "__main__":
    import sys

    if "--create-template" in sys.argv:
        create_template_file()
    else:
        print_search_queries()

        # Check if manual_urls.txt exists
        import os
        if not os.path.exists('manual_urls.txt'):
            print("\n💡 TIP: Run with --create-template to create manual_urls.txt")
            print("   python claude_search_assistant.py --create-template")
