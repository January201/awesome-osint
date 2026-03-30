#!/usr/bin/env python3
"""
Remove duplicate entries from README.md
Keeps the first occurrence of each duplicate (case-insensitive) and removes subsequent ones.
"""

import re
import sys

def normalize_name(name):
    """Normalize name for comparison (lowercase, strip whitespace)."""
    return name.lower().strip()

def remove_duplicates(filepath, output_path=None):
    if output_path is None:
        output_path = filepath
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    seen_names = set()
    duplicates_removed = 0
    output_lines = []
    
    # Pattern to match list items with links: * [Name](url) or - [Name](url)
    link_pattern = re.compile(r'^\s*\*?\s*\[([^\]]+)\]\([^)]+\)')
    # Pattern to match simple list items: * Name or - Name
    simple_pattern = re.compile(r'^\s*\*?\s*([^\[\]\n]+?)(?:\s*$|\s+#|\s+\|)')
    
    for line in lines:
        # Check if this is a list item
        if line.strip().startswith('*') or line.strip().startswith('-'):
            # Try to extract name from link format
            match = link_pattern.match(line)
            if match:
                entry_name = match.group(1).strip()
            else:
                # Try simple format
                match = simple_pattern.match(line)
                if match:
                    entry_name = match.group(1).strip()
                else:
                    entry_name = None
            
            if entry_name:
                normalized_name = normalize_name(entry_name)
                
                # Skip arrow links (↑)
                if normalized_name == '↑':
                    output_lines.append(line)
                    continue
                
                # Check if we've seen this name before
                if normalized_name in seen_names:
                    # This is a duplicate - skip it
                    duplicates_removed += 1
                    print(f"  Removing duplicate: '{entry_name}'")
                    continue
                else:
                    # First occurrence - keep it
                    seen_names.add(normalized_name)
            
            output_lines.append(line)
        else:
            output_lines.append(line)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"\n{'='*60}")
    print(f"DUPLICATE REMOVAL COMPLETE")
    print(f"{'='*60}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Output written to: {output_path}")
    
    return duplicates_removed

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 remove_duplicates.py <readme_file> [output_file]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    remove_duplicates(filepath, output_path)
