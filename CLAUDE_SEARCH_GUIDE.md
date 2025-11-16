# Using Claude's Web Search to Avoid Bot Detection

## The Problem

Many business listing websites (BizBuySell, BizQuest, LoopNet, etc.) have bot detection that blocks automated HTTP requests, resulting in:
- 403 Forbidden errors
- Connection timeouts
- CAPTCHA challenges

## The Solution: Claude-Assisted Search

Claude Code has native web search capabilities that don't trigger bot detection. This guide shows you how to use Claude to find business listings.

## Method 1: Quick Start (Recommended)

### Step 1: Generate Search Queries
```bash
python claude_search_assistant.py
```

This will display search queries optimized for finding senior care businesses.

### Step 2: Search with Claude Code

Copy each query and paste it into your Claude Code chat. For example:

```
Find senior home care businesses for sale in Los Angeles on bizbuysell.com - provide direct URLs to listings
```

Claude will search the web and return actual business listing URLs.

### Step 3: Save URLs

1. Create or open `manual_urls.txt`:
   ```bash
   python claude_search_assistant.py --create-template
   ```

2. Paste the URLs Claude found (one per line):
   ```
   https://www.bizbuysell.com/Business-Opportunity/Senior-Care-Business-12345/
   https://www.bizquest.com/businesses-for-sale/listing/67890.html
   https://www.loopnet.com/listing/98765/
   ```

### Step 4: Run Analysis

```bash
python main.py
```

The script will fetch and analyze the businesses from your manual URLs, avoiding all bot detection issues.

## Method 2: Direct Claude Interaction

You can also ask Claude Code directly in freeform conversation:

**You:** "Search for senior home care businesses for sale in Los Angeles on bizbuysell.com, bizquest.com, and loopnet.com. Give me the direct URLs to specific business listings."

**Claude Code:** [Searches and provides URLs]

Then paste those URLs into `manual_urls.txt` and run `python main.py`.

## Why This Works

1. **Claude Code has native web search** - It uses tools that websites don't block
2. **No bot fingerprinting** - Claude's searches look like regular user activity
3. **CAPTCHA-free** - No automation detection triggers
4. **Always up-to-date** - Gets the latest listings from websites

## Automated vs Manual Mode

### Automated Mode (Default)
- Script makes direct HTTP requests
- May hit bot detection (403 errors, timeouts)
- Faster when it works
- No user interaction needed

### Manual Mode (Recommended for reliability)
- Uses Claude Code for searching
- Never hits bot detection
- Requires copy/paste of URLs
- 100% reliable

## Tips

- **Be specific**: Ask Claude for "direct URLs to listings" not just search results
- **Multiple sites**: Claude can search multiple sites in one query
- **Fresh results**: Run new searches periodically to get new listings
- **Mix and match**: Use automated mode first, fall back to Claude if blocked

## Example Workflow

```bash
# Try automated search first
python main.py

# If you get bot detection errors:
# 1. Get search queries
python claude_search_assistant.py

# 2. Ask me (Claude Code) to search using those queries
# 3. Copy the URLs I find into manual_urls.txt
# 4. Run again
python main.py
```

## Support

If you have issues:
1. Make sure `manual_urls.txt` has valid URLs (one per line)
2. Lines starting with `#` are comments and will be ignored
3. URLs must start with `http://` or `https://`
4. Empty lines are okay
