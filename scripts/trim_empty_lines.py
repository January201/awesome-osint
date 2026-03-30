#!/usr/bin/env python3
"""
Remove excessive empty lines from README.md
Keeps maximum of 2 consecutive empty lines
"""

import re

def trim_empty_lines(filepath, output_path=None):
    if output_path is None:
        output_path = filepath
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count before
    total_lines = len(content.split('\n'))
    empty_lines_before = len(re.findall(r'\n\s*\n\s*\n', content))
    
    # Replace 3+ consecutive newlines with 2
    trimmed = re.sub(r'\n\s*\n\s*\n\s*\n', '\n\n\n', content)
    trimmed = re.sub(r'\n\s*\n\s*\n\s*\n', '\n\n\n', trimmed)  # Run twice for safety
    
    # Count after
    empty_lines_after = len(re.findall(r'\n\s*\n\s*\n', trimmed))
    removed = empty_lines_before - empty_lines_after
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(trimmed)
    
    print(f"Trimmed empty lines:")
    print(f"  Before: ~{empty_lines_before} excessive empty line groups")
    print(f"  After: ~{empty_lines_after} excessive empty line groups")
    print(f"  Removed: {removed} groups")
    print(f"  Total lines: {total_lines}")
    
    return removed

if __name__ == '__main__':
    trim_empty_lines('/workspace/README.md')
