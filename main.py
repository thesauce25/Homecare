#!/usr/bin/env python3
"""
Senior Home Care Business Finder
Main application entry point
"""
import sys
from datetime import datetime
import config
from search_engine import BusinessSearcher
from claude_analyzer import ClaudeAnalyzer
from excel_handler import ExcelHandler


def print_banner():
    """Print application banner."""
    print("=" * 70)
    print(" Senior Home Care Business Finder ".center(70, "="))
    print("=" * 70)
    print(f"Location: {config.SEARCH_LOCATION}")
    print(f"Output File: {config.EXCEL_FILENAME}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


def main():
    """Main application logic."""
    try:
        # Validate configuration
        config.validate_config()

        # Print banner
        print_banner()

        # Initialize components
        searcher = BusinessSearcher()
        analyzer = ClaudeAnalyzer()
        excel_handler = ExcelHandler()

        # Show existing data summary
        print("\n=== Current Data Summary ===")
        summary = excel_handler.get_summary()
        if summary['file_exists']:
            print(f"Existing businesses in spreadsheet: {summary['total_businesses']}")
        else:
            print("No existing spreadsheet found - will create new one")

        # Step 1: Search for businesses
        print("\n=== Step 1: Searching for Senior Care Businesses ===")
        search_results = searcher.search_for_businesses()

        if not search_results:
            print("❌ No search results found.")
            print("\n💡 TIP: To avoid bot detection, use Claude's web search:")
            print("   1. Run: python claude_search_assistant.py")
            print("   2. Use Claude Code to find business URLs")
            print("   3. Add URLs to manual_urls.txt")
            print("   4. Run this script again")
            return 1

        # Step 2: Analyze with Claude
        print("\n=== Step 2: Analyzing Results with Claude AI ===")
        businesses = analyzer.analyze_search_results(search_results)

        if not businesses:
            print("❌ No senior care businesses found in search results.")
            return 1

        print(f"\n✓ Found {len(businesses)} senior care businesses")

        # Step 3: Save to Excel
        print("\n=== Step 3: Saving to Excel ===")
        new_count = excel_handler.append_businesses(businesses)

        # Final summary
        print("\n" + "=" * 70)
        print(" Results Summary ".center(70, "="))
        print("=" * 70)
        print(f"Total businesses analyzed: {len(businesses)}")
        print(f"New businesses added: {new_count}")
        print(f"Duplicates skipped: {len(businesses) - new_count}")

        final_summary = excel_handler.get_summary()
        print(f"Total businesses in spreadsheet: {final_summary['total_businesses']}")
        print(f"\n✓ Results saved to: {config.EXCEL_FILENAME}")
        print("=" * 70)

        return 0

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file (copy from .env.example)")
        print("2. Added your ANTHROPIC_API_KEY to the .env file")
        return 1

    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        return 1

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
