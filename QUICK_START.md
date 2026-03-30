# Quick Start Guide

Welcome to the improved Awesome OSINT repository! This guide helps you get started quickly.

## For Contributors

### Adding a New Tool

1. **Check for duplicates first**
   ```bash
   python3 scripts/check_duplicates.py README.md
   ```

2. **Ensure your link uses HTTPS** (not HTTP)

3. **Follow the format**:
   ```markdown
   * [Tool Name](https://example.com) - Brief description of what it does
   ```

4. **Place in correct category** - See Table of Contents

5. **Submit via Issue or PR** using our templates

### Before Submitting a PR

Run these validation checks:

```bash
# Check format (must pass with 0 errors)
python3 scripts/validate_format.py README.md

# Check for duplicates (warning if found)
python3 scripts/check_duplicates.py README.md

# Check alphabetization (warning if issues)
python3 scripts/check_alphabetization.py README.md
```

All checks should pass before submission!

## For Users

### Finding Tools

1. Use the **Table of Contents** at the top of README.md
2. Search within the file (Ctrl+F / Cmd+F)
3. Check our categorized sections

### Reporting Issues

Found a broken link or duplicate? 

1. Go to Issues tab
2. Click "New Issue"
3. Select "Report Issue" template
4. Fill in the details

## Repository Structure

```
awesome-osint/
├── README.md                    # Main list (1,750 lines)
├── CONTRIBUTING.md              # Contribution guidelines
├── CODE_OF_CONDUCT.md           # Community standards
├── SECURITY.md                  # Security policy
├── IMPLEMENTATION_STATUS.md     # Current improvement status
├── .github/
│   ├── workflows/               # CI/CD pipelines
│   │   ├── link-check.yml      # Weekly link validation
│   │   └── format-validator.yml # PR format checks
│   ├── ISSUE_TEMPLATE/          # Issue templates
│   │   ├── add-tool.yml        # Add new tool form
│   │   └── report-issue.yml    # Report problems form
│   └── pull_request_template.md # PR checklist
└── scripts/                     # Validation scripts
    ├── validate_format.py       # Format checker
    ├── check_duplicates.py      # Duplicate finder
    ├── check_alphabetization.py # Alphabetization checker
    ├── trim_empty_lines.py      # Cleanup utility
    └── remove_trailing_whitespace.py # Whitespace cleanup
```

## Quality Standards

✅ **Required for all submissions:**
- HTTPS URLs only
- No duplicates
- Proper markdown format
- Correct category placement
- Active/maintained tools preferred

❌ **Will be rejected:**
- HTTP links
- Duplicate entries
- Malformed markdown
- Broken links
- Spam or affiliate links

## Automation

Our CI/CD automatically checks:
- ✅ Link validity (weekly)
- ✅ Format compliance (every PR)
- ✅ Duplicate detection (every PR)
- ✅ Alphabetization (every PR)

## Need Help?

- 📖 Read [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines
- 🔒 Review [SECURITY.md](./SECURITY.md) for security policies
- 🤝 Follow [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) for community standards
- 📊 Check [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md) for current progress

---

**Thank you for contributing to Awesome OSINT!** 🎉
