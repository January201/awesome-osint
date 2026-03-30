#!/usr/bin/env python3
"""
Automatically fix alphabetization issues in README.md
Sorts entries within each section alphabetically (case-insensitive)
"""

import re
import sys

def extract_entry_name(line):
    """Extract the tool name from a markdown list item."""
    match = re.match(r'^\s*\*?\s*\[([^\]]+)\]\([^)]+\)', line)
    if match:
        return match.group(1).strip()
    return None

def sort_section(entries):
    """Sort entries alphabetically by tool name (case-insensitive)."""
    return sorted(entries, key=lambda x: extract_entry_name(x).lower() if extract_entry_name(x) else '')

def fix_alphabetization(filepath, output_path=None):
    if output_path is None:
        output_path = filepath
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    current_section_entries = []
    in_section = False
    sections_processed = 0
    entries_sorted = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a section header (### or ##)
        if line.startswith('##'):
            # If we were collecting entries, sort and add them
            if current_section_entries:
                sorted_entries = sort_section(current_section_entries)
                if sorted_entries != current_section_entries:
                    entries_sorted += len(sorted_entries)
                    print(f"  Sorted {len(sorted_entries)} entries in section")
                output_lines.extend(sorted_entries)
                current_section_entries = []
            
            output_lines.append(line)
            in_section = True
            sections_processed += 1
        
        # Check if this is a list item
        elif in_section and (line.strip().startswith('*') or line.strip().startswith('-')):
            # Check if it's an entry (has a link) or just text/separator
            if extract_entry_name(line):
                current_section_entries.append(line)
            else:
                # Not a valid entry, flush current entries first
                if current_section_entries:
                    sorted_entries = sort_section(current_section_entries)
                    if sorted_entries != current_section_entries:
                        entries_sorted += len(sorted_entries)
                    output_lines.extend(sorted_entries)
                    current_section_entries = []
                output_lines.append(line)
        
        # Empty line or other content
        elif line.strip() == '':
            if current_section_entries:
                sorted_entries = sort_section(current_section_entries)
                if sorted_entries != current_section_entries:
                    entries_sorted += len(sorted_entries)
                output_lines.extend(sorted_entries)
                current_section_entries = []
            output_lines.append(line)
        
        else:
            # Other content (description text, etc.)
            if current_section_entries:
                sorted_entries = sort_section(current_section_entries)
                if sorted_entries != current_section_entries:
                    entries_sorted += len(sorted_entries)
                output_lines.extend(sorted_entries)
                current_section_entries = []
            output_lines.append(line)
        
        i += 1
    
    # Don't forget any remaining entries
    if current_section_entries:
        sorted_entries = sort_section(current_section_entries)
        if sorted_entries != current_section_entries:
            entries_sorted += len(sorted_entries)
        output_lines.extend(sorted_entries)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"\n{'='*60}")
    print(f"ALPHABETIZATION FIX COMPLETE")
    print(f"{'='*60}")
    print(f"Sections processed: {sections_processed}")
    print(f"Entries sorted: {entries_sorted}")
    print(f"Output written to: {output_path}")
    
    return entries_sorted

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 fix_alphabetization.py <readme_file> [output_file]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    fix_alphabetization(filepath, output_path)
