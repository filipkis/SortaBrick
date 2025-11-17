# Claude Code Instructions for This Project

## Auto-Commit Policy

**IMPORTANT: Automatically commit changes after completing each task.**

After finishing any user-requested task that modifies files:

1. Stage all changes: `git add -A`
2. Review what's being committed: `git diff --cached --stat`
3. Create a descriptive commit message that includes:
   - Clear summary of what was changed
   - List of key modifications
   - New files added (if any)
   - The Claude Code attribution footer
4. Commit the changes
5. Confirm the commit was created

### Example Commit Message Format

```
Brief description of changes

- Detailed point about change 1
- Detailed point about change 2
- List of new files added
- List of updated files

New files:
- path/to/new/file.py: Description

Updated files:
- path/to/updated/file.py: What changed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### When NOT to Commit

- During exploration/research tasks (just reading files)
- When explicitly told not to commit
- When the user says "don't commit this yet"

### Verification

After committing, always show:
- Commit hash
- Number of files changed
- Brief summary of what was committed

---

## Project-Specific Context

This is a LEGO piece identification tool that:
- Segments photos of LEGO pieces
- Identifies pieces using Brickognize API
- Generates HTML review pages with Rebrickable images
- Requires Rebrickable API key for image fetching

Key technologies:
- Python 3.8+
- OpenCV for image processing
- Brickognize API for identification
- Rebrickable API for part images
