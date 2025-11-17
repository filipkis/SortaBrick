# Contributing to LEGO Sorter

## Development Workflow

### Working with Claude Code

This project uses Claude Code for development assistance. Claude is configured to:

- **Automatically commit changes** after completing each task
- Follow the project's coding standards
- Generate descriptive commit messages with the Claude Code attribution

The configuration is stored in `.claude/instructions.md`.

### Making Changes

1. Make your changes to the code
2. Test the changes work correctly
3. Changes will be automatically committed by Claude (if using Claude Code)
4. Or manually commit: `git add -A && git commit -m "Your message"`

### Commit Message Format

We use descriptive commit messages that include:
- Clear summary of changes
- Bulleted list of key modifications
- List of new/updated files
- Attribution footer (when using Claude Code)

Example:
```
Add feature X for better Y processing

- Implement new algorithm for X
- Update documentation
- Add tests for feature X

New files:
- src/feature_x.py: Main implementation

Updated files:
- README.md: Add documentation for feature X

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Testing

Before committing, verify:
- Code runs without errors
- Tests pass (if applicable)
- Documentation is updated
- API keys are not committed (.gitignore is configured)

### Code Style

- Follow PEP 8 for Python code
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### Adding Dependencies

If adding new Python dependencies:
1. Add to `requirements.txt`
2. Document in README if it requires setup
3. Test on a clean environment

### Documentation

Update documentation when:
- Adding new features
- Changing existing behavior
- Adding new configuration options
- Adding new API integrations

Key documentation files:
- `README.md` - Main project documentation
- `REBRICKABLE_SETUP.md` - Rebrickable API setup
- `REVIEW_FEATURE.md` - Review feature documentation
- `.claude/instructions.md` - Claude Code configuration

## Project Structure

```
legosorter/
├── .claude/              # Claude Code configuration
├── src/                  # Source code
│   ├── main.py          # Main workflow
│   ├── segmentation.py  # Image processing
│   ├── api_client.py    # Brickognize API
│   ├── rebrickable_client.py  # Rebrickable API
│   └── review_generator.py    # HTML review generation
├── input/               # Input images
├── output/              # Generated results
└── docs/                # Documentation
```

## Getting Help

- Check the README for setup instructions
- Review existing code for patterns
- Check documentation files for specific features
- Open an issue for bugs or feature requests
