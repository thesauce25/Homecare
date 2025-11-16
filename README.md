# Senior Home Care Business Finder

An automated tool that uses Claude AI to search for senior home care businesses for sale in Southern California (Los Angeles area) and exports the results to an Excel spreadsheet.

## Features

- 🔍 Two search modes: automated web search OR manual URL list
- 📊 Exports results to Excel with detailed information
- 🔄 Appends new results without duplicating existing entries
- 🤖 Uses Claude AI to analyze and extract business information
- 🎯 Focuses on LA/Southern California senior home care businesses

## Excel Output Columns

- **Business Name**: Name of the senior care business
- **Financial Info**: Revenue, EBITDA, asking price, and other financial details
- **Listing Link**: URL to the business listing
- **Broker Info**: Broker name and contact information
- **Date Added**: When the listing was found and added

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Anthropic API key:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

3. Run the application:
```bash
python main.py
```

## Two Search Modes

### Automatic Mode (Default)
The app automatically searches BizBuySell, LoopNet, BizQuest, and DealStream for listings.

### Manual Mode
If automatic search has issues, or you want to analyze specific listings:

1. Open `manual_urls.txt`
2. Add business listing URLs (one per line)
3. Run `python main.py` - it will analyze your URLs instead of searching

Example manual_urls.txt:
```
https://www.bizbuysell.com/Business-Opportunity/Some-Business-123456/
https://www.loopnet.com/listing/some-listing-789/
```

## Configuration

Edit `config.py` to customize:
- Search location (default: Los Angeles, Southern California)
- Excel output filename
- Number of search results to process
- Claude model settings

## Output

Results are saved to `senior_care_businesses.xlsx` in the project directory. Each run appends new unique listings to the existing file.

## Requirements

- Python 3.8+
- Anthropic API key
- Internet connection for web searches
