# Rebrickable Images Update

## What Changed

The review feature now uses **Rebrickable API** instead of BrickLink URLs to fetch official LEGO part images. This provides reliable, high-quality images directly from Rebrickable's database.

## Why This Change?

- ✓ **BrickLink has no official API** - the old approach used constructed URLs that may not work
- ✓ **Rebrickable has a free, official API** - reliable and well-documented
- ✓ **Better image quality** - official part images from Rebrickable's database
- ✓ **Additional metadata** - get part names and descriptions too
- ✓ **Consistent with workflow** - you're likely using Rebrickable to track your collection anyway

## Quick Setup (5 minutes)

### Step 1: Get Your Free API Key

1. Go to https://rebrickable.com/api/
2. Log in or create a free account
3. Scroll to "Your API Key" section
4. Copy your API key

### Step 2: Configure the Key

**Option A - Environment Variable (Recommended):**
```bash
export REBRICKABLE_API_KEY='your_key_here'
```

**Option B - Key File (Simple):**
```bash
echo "your_key_here" > .rebrickable_key
```

### Step 3: You're Done!

Run your workflow as normal:
```bash
python main.py input/lego_pieces.jpg
```

Images will be automatically fetched from Rebrickable when generating the review page.

## What Happens During Review Generation

1. **Extracts part numbers** from identification results
2. **Batches API requests** to Rebrickable for all unique parts
3. **Fetches image URLs and metadata** for each part
4. **Caches results** to avoid duplicate requests
5. **Generates HTML** with embedded Rebrickable images

## Example Output

Before (BrickLink URL approach):
```
❌ Images may not load (no official API)
❌ No part names or metadata
```

After (Rebrickable API):
```
✓ Fetching part images from Rebrickable API...
  Fetching part info: 10/15
✓ Fetched images for 15 parts
✓ Review page saved to: output/results/review.html
```

## API Usage

### Free Tier Limits
- **1,000 requests per day** (very generous)
- **~10 requests per second** rate limit

### Typical Usage
- 20 pieces with 3 predictions each = ~60 API requests
- You can process hundreds of pieces per day

### Optimizations
- ✓ **Automatic caching** - same part fetched only once
- ✓ **Rate limiting** - respectful of API limits
- ✓ **Batch fetching** - efficient parallel requests

## Working Without API Key

If you don't set up the API key, the tool still works but:

- Shows **placeholder images** with part numbers
- Still includes **clickable links** to Rebrickable and BrickLink
- You can **add the API key later** and regenerate reviews

To generate review without fetching images:
```bash
python generate_review.py results.json --no-rebrickable
```

## Troubleshooting

### "Rebrickable API key required" Warning

The tool will continue with placeholders. To fix:
1. Get API key from https://rebrickable.com/api/
2. Set `REBRICKABLE_API_KEY` environment variable
3. Or create `.rebrickable_key` file

### API Request Fails

- Check internet connection
- Verify API key is valid
- Check if you've exceeded daily limit (unlikely - 1000 req/day)

### Some Images Missing

- Rare or very old parts may not have images in Rebrickable
- Placeholders with part numbers will be shown instead
- This is normal and expected

## Migration from Old Setup

If you were using the old system:

1. **No changes needed** to your existing workflow
2. **Add API key** to enable images (5 minutes)
3. **Regenerate old reviews** with images:
   ```bash
   python generate_review.py old_results.json
   ```

## Benefits

✓ **Reliable images** - official API, not URL hacking
✓ **Better metadata** - part names and descriptions
✓ **Free forever** - Rebrickable's free tier is generous
✓ **Future-proof** - official API won't break
✓ **Better UX** - tooltip shows part name on hover

## File Changes

New files:
- `src/rebrickable_client.py` - API client
- `.rebrickable_key.example` - Key file template
- `REBRICKABLE_SETUP.md` - Detailed setup guide

Updated files:
- `src/review_generator.py` - Now uses Rebrickable API
- `README.md` - Updated installation instructions
- `.gitignore` - Excludes `.rebrickable_key` file

No changes to:
- Segmentation algorithm
- Identification workflow (Brickognize API)
- JSON output format
- Text results format
