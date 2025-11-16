"""Configuration settings for the Senior Home Care Business Finder."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Anthropic API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"

# Search Configuration
SEARCH_LOCATION = "Los Angeles, Southern California"
SEARCH_QUERY_TEMPLATE = "senior home care businesses for sale {location}"
MAX_SEARCH_RESULTS = 20  # Number of results to process per run

# Excel Configuration
EXCEL_FILENAME = "senior_care_businesses.xlsx"
EXCEL_COLUMNS = [
    "Business Name",
    "Financial Info",
    "Listing Link",
    "Broker Info",
    "Date Added",
    "Additional Notes"
]

# Search Sources - Common business-for-sale websites
SEARCH_SOURCES = [
    "bizbuysell.com",
    "businessbroker.net",
    "bizquest.com",
    "sunbeltnetwork.com"
]

def validate_config():
    """Validate that required configuration is present."""
    if not ANTHROPIC_API_KEY:
        raise ValueError(
            "ANTHROPIC_API_KEY not found. Please set it in your .env file. "
            "Get your API key from: https://console.anthropic.com/"
        )
    return True
