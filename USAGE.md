# Usage Guide

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up API Key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Anthropic API key
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

## How It Works

The application follows a three-step process:

### Step 1: Web Search
- Searches multiple business-for-sale websites (BizBuySell, BizQuest, etc.)
- Focuses on Los Angeles and Southern California
- Looks specifically for senior care and home care businesses

### Step 2: Claude AI Analysis
- Uses Claude AI to analyze each search result
- Extracts structured business information:
  - Business name
  - Financial details (asking price, revenue, EBITDA, etc.)
  - Broker contact information
  - Location and other relevant details
- Filters out non-relevant listings

### Step 3: Excel Export
- Saves results to `senior_care_businesses.xlsx`
- Automatically avoids duplicates based on listing URLs
- Appends new results to existing file
- Formats data with headers and clickable links

## Excel Output Format

| Column | Description |
|--------|-------------|
| Business Name | Name of the senior care business |
| Financial Info | Asking price, revenue, EBITDA, cash flow, etc. |
| Listing Link | Clickable URL to the full business listing |
| Broker Info | Broker name, company, and contact details |
| Date Added | Date when the listing was added to spreadsheet |
| Additional Notes | Location, years in business, size, etc. |

## Customization

Edit `config.py` to customize:

- **SEARCH_LOCATION**: Change the target location
- **MAX_SEARCH_RESULTS**: Adjust number of listings to process per run
- **EXCEL_FILENAME**: Change the output filename
- **SEARCH_SOURCES**: Add or remove business listing websites

## Running Periodically

To keep your spreadsheet updated with new listings, you can:

### Option 1: Manual Runs
```bash
# Run weekly or as needed
python main.py
```

### Option 2: Cron Job (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add line to run every Monday at 9 AM
0 9 * * 1 cd /path/to/Homecare && python main.py
```

### Option 3: Task Scheduler (Windows)
Create a scheduled task to run `python main.py` at your desired frequency.

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Make sure you created a `.env` file
- Verify your API key is correctly set in the `.env` file
- Get your API key from: https://console.anthropic.com/

### "No search results found"
- Check your internet connection
- Some websites may have rate limiting - try again later
- The search URLs in `search_engine.py` may need updating

### "No businesses found"
- Claude filtered out all results as non-relevant
- Try adjusting the search parameters in `config.py`
- Check if the target websites changed their structure

## API Costs

The application uses Claude AI to analyze web content. Typical costs per run:
- ~10-20 API calls per run (depending on MAX_SEARCH_RESULTS)
- Each call processes web page content
- Estimated cost: $0.10 - $0.50 per run (with Claude Sonnet)

To reduce costs:
- Lower `MAX_SEARCH_RESULTS` in config.py
- Run less frequently
- Use a less expensive model (edit CLAUDE_MODEL in config.py)

## Support

For issues or questions:
1. Check this usage guide
2. Review the code comments in each module
3. Verify your API key and dependencies are correctly set up
