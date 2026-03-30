#!/usr/bin/env python3
"""
Validate format of README.md entries
Checks for:
- Consistent markdown link format
- Proper spacing and punctuation
- No trailing whitespace
- No excessive empty lines
"""

import re
import sys

def validate_format(filepath):
    errors = []
    warnings = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Check for trailing whitespace
    for i, line in enumerate(lines, 1):
        if line.rstrip() != line.rstrip('\n').rstrip():
            errors.append(f"Line {i}: Trailing whitespace detected")
    
    # Check for excessive empty lines (more than 2 consecutive)
    empty_count = 0
    for i, line in enumerate(lines, 1):
        if line.strip() == '':
            empty_count += 1
            if empty_count > 2:
                errors.append(f"Line {i}: Excessive empty lines (more than 2 consecutive)")
        else:
            empty_count = 0
    
    # Check for malformed links
    # Valid format: * [Name](https://url) - Description
    # or: * [Name](https://url)
    link_pattern = r'\*\s*\[([^\]]+)\]\(([^)]+)\)'
    malformed_pattern = r'\*\s*\[([^\]]+)\]\s*[^(]'
    
    for i, line in enumerate(lines, 1):
        # Skip headers and non-list lines
        if not line.strip().startswith('*'):
            continue
        
        # Check for proper link format
        if '[' in line and ']' in line:
            if not re.search(link_pattern, line):
                if re.search(malformed_pattern, line):
                    errors.append(f"Line {i}: Malformed link - missing parentheses around URL")
    
    # Check for HTTP links (should be HTTPS)
    http_pattern = r'\]\(http://'
    for i, line in enumerate(lines, 1):
        if re.search(http_pattern, line):
            errors.append(f"Line {i}: Uses HTTP instead of HTTPS")
    
    # Check for inconsistent bullet points
    bullet_variations = [r'^\s+-\s', r'^\s*\*\s', r'^\s*-\s*\[' ]
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('- ') and '[' in line:
            warnings.append(f"Line {i}: Inconsistent bullet point (use '*' not '-')")
    
    # Print results
    print("=" * 60)
    print("FORMAT VALIDATION RESULTS")
    print("=" * 60)
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for error in errors[:20]:  # Show first 20 errors
            print(f"  {error}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")
    else:
        print("\n✅ No errors found!")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings[:10]:  # Show first 10 warnings
            print(f"  {warning}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more warnings")
    
    print("\n" + "=" * 60)
    print(f"Total: {len(errors)} errors, {len(warnings)} warnings")
    print("=" * 60)
    
    return len(errors) == 0

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'README.md'
    success = validate_format(filepath)
    sys.exit(0 if success else 1)
