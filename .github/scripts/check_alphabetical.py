#!/usr/bin/env python3
"""
Check if list items in README.md are sorted alphabetically within each section.
"""

import re
import sys
from pathlib import Path

def extract_list_items(content):
    """Extract list items grouped by section."""
    sections = {}
    current_section = None
    current_items = []
    
    for line in content.split('\n'):
        # Check for section headers (## Header)
        header_match = re.match(r'^##\s+(?:\[.*?\]\(.*?\)\s+)?(.+)$', line)
        if header_match:
            if current_section and current_items:
                sections[current_section] = current_items
            current_section = header_match.group(1).strip()
            current_items = []
        
        # Check for list items (* or -)
        list_match = re.match(r'^[\*\-]\s+\[([^\]]+)\]', line)
        if list_match and current_section:
            item_name = list_match.group(1).strip()
            # Remove "The " prefix for sorting comparison
            sort_name = re.sub(r'^The\s+', '', item_name, flags=re.IGNORECASE)
            current_items.append((item_name, sort_name, line))
    
    # Don't forget the last section
    if current_section and current_items:
        sections[current_section] = current_items
    
    return sections

def check_alphabetical(sections):
    """Check if items in each section are alphabetically sorted."""
    errors = []
    
    for section, items in sections.items():
        if len(items) < 2:
            continue
        
        sort_names = [item[1] for item in items]
        sorted_names = sorted(sort_names, key=str.lower)
        
        if sort_names != sorted_names:
            errors.append(f"Section '{section}' is not alphabetically sorted")
            for i, (original, sort_name, line) in enumerate(items):
                expected_pos = sorted_names.index(sort_name)
                if i != expected_pos:
                    errors.append(f"  Line {i+1}: '{original}' should be at position {expected_pos+1}")
    
    return errors

def main():
    readme_path = Path('README.md')
    
    if not readme_path.exists():
        print(f"Error: {readme_path} not found")
        sys.exit(1)
    
    content = readme_path.read_text()
    sections = extract_list_items(content)
    errors = check_alphabetical(sections)
    
    if errors:
        print("❌ Alphabetical order issues found:")
        for error in errors:
            print(error)
        sys.exit(1)
    else:
        print("✅ All sections are alphabetically sorted")
        sys.exit(0)

if __name__ == '__main__':
    main()
