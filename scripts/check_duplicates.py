#!/usr/bin/env python3
"""
Check for duplicate entries in README.md
Duplicates are identified by normalized tool names (case-insensitive)
Only checks list items (lines starting with * or -), not inline links
"""

import re
import sys
from collections import defaultdict

def check_duplicates(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Extract tool names only from list items (lines starting with * or -)
    pattern = r'^\s*\*?\s*\[([^\]]+)\]\([^)]+\)'
    matches = []
    
    for line in lines:
        match = re.match(pattern, line, re.IGNORECASE)
        if match:
            matches.append(match.group(1))
    
    # Normalize names (lowercase, strip whitespace)
    normalized = defaultdict(list)
    for name in matches:
        key = name.strip().lower()
        normalized[key].append(name)
    
    # Find duplicates
    duplicates = {k: v for k, v in normalized.items() if len(v) > 1}
    
    print("=" * 60)
    print("DUPLICATE CHECK RESULTS")
    print("=" * 60)
    
    if duplicates:
        print(f"\n❌ Found {len(duplicates)} duplicate entries:\n")
        for key, occurrences in sorted(duplicates.items()):
            unique_names = list(set(occurrences))
            print(f"  '{key}' appears {len(occurrences)} time(s):")
            for name in unique_names[:3]:
                print(f"    - {name}")
            if len(unique_names) > 3:
                print(f"    ... and {len(unique_names) - 3} more variations")
            print()
    else:
        print("\n✅ No duplicates found!")
    
    print("=" * 60)
    print(f"Total entries checked: {len(matches)}")
    print(f"Unique entries: {len(normalized)}")
    print(f"Duplicates: {len(duplicates)}")
    print("=" * 60)
    
    return len(duplicates) == 0

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'README.md'
    success = check_duplicates(filepath)
    sys.exit(0 if success else 1)
