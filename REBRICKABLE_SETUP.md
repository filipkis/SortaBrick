# Rebrickable API Setup

The review feature uses the Rebrickable API to fetch official LEGO part images. This requires a free API key.

## Getting Your API Key

1. **Create a Rebrickable account** (if you don't have one):
   - Go to https://rebrickable.com/
   - Click "Sign Up" and create a free account

2. **Get your API key**:
   - Log in to Rebrickable
   - Go to https://rebrickable.com/api/
   - Scroll down to the "Your API Key" section
   - Copy your API key (looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

## Setting Up the API Key

You have **three options** to provide your API key:

### Option 1: Environment Variable (Recommended)

Set the `REBRICKABLE_API_KEY` environment variable:

**macOS/Linux:**
```bash
# Temporary (current session only)
export REBRICKABLE_API_KEY='your_api_key_here'

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export REBRICKABLE_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
# Temporary (current session only)
$env:REBRICKABLE_API_KEY = "your_api_key_here"

# Permanent (system-wide)
[System.Environment]::SetEnvironmentVariable('REBRICKABLE_API_KEY', 'your_api_key_here', 'User')
```

### Option 2: Key File (Simple)

Create a file named `.rebrickable_key` in the project root:

```bash
# In the legosorter directory
echo "your_api_key_here" > .rebrickable_key
```

This file is already in `.gitignore` so it won't be committed to version control.

### Option 3: Pass as Parameter (Advanced)

Pass the API key directly when generating reviews:

```python
from review_generator import generate_review_html

generate_review_html(results, output_path, api_key="your_api_key_here")
```

## Verifying Your Setup

Test that your API key works:

```bash
cd src
python -c "from rebrickable_client import RebrickableClient; client = RebrickableClient(); print('✓ API key is valid!' if client.get_part_info('3001') else '✗ Failed')"
```

If successful, you should see: `✓ API key is valid!`

## Using Without API Key

If you don't want to use the Rebrickable API, the review page will still work but will show placeholder images instead of actual LEGO part images.

To disable Rebrickable image fetching:

```bash
# When generating reviews manually
python generate_review.py results.json --no-rebrickable
```

Or in code:
```python
generate_review_html(results, output_path, use_rebrickable=False)
```

## API Usage Limits

Rebrickable's free tier includes:
- **1,000 requests per day**
- Rate limiting: ~10 requests per second

This is more than enough for typical usage. The tool automatically:
- Caches results to avoid duplicate requests
- Rate limits requests to be respectful
- Only fetches images for parts that appear in your results

For a typical batch of 20 pieces with 3 predictions each, you'll use ~60 API requests.

## Troubleshooting

**"Rebrickable API key required" error:**
- Make sure you've set up your API key using one of the three methods above
- Verify the key is correct (no extra spaces or quotes)

**"Could not fetch Rebrickable data" warning:**
- Check your internet connection
- Verify your API key is valid at https://rebrickable.com/api/
- Check if you've exceeded the daily limit (1000 requests)

**Images not showing:**
- Some older or rare parts may not have images in Rebrickable
- The tool will show a placeholder with the part number instead

**Rate limiting errors:**
- The tool automatically rate-limits requests
- If you still see errors, you may have other applications using the API
- Wait a few minutes and try again
