#!/usr/bin/env python3
"""
Check alphabetization within sections of README.md
Each section should have entries sorted alphabetically by tool name
"""

import re
import sys

def check_alphabetization(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    errors = []
    current_section = None
    current_entries = []
    
    # Pattern to detect section headers (## Header)
    section_pattern = r'^##\s+(?:\[.+\]\([^)]+\)\s+)?(.+)$'
    # Pattern to detect list items with links
    entry_pattern = r'^\*\s*\[([^\]]+)\]'
    
    def check_section(section_name, entries):
        """Check if entries in a section are alphabetized"""
        if len(entries) < 2:
            return []
        
        section_errors = []
        names = [name for _, name in entries]
        normalized = [name.lower().strip() for name in names]
        
        # Check if sorted
        if normalized != sorted(normalized):
            # Find specific out-of-order entries
            for i in range(len(normalized) - 1):
                if normalized[i] > normalized[i + 1]:
                    section_errors.append({
                        'section': section_name,
                        'line': entries[i][0],
                        'current': names[i],
                        'next': names[i + 1]
                    })
        
        return section_errors
    
    for i, line in enumerate(lines, 1):
        # Check for section header
        section_match = re.match(section_pattern, line.strip())
        if section_match:
            # Check previous section before starting new one
            if current_section and current_entries:
                errors.extend(check_section(current_section, current_entries))
            
            current_section = section_match.group(1).strip()
            current_entries = []
            continue
        
        # Check for entry
        entry_match = re.match(entry_pattern, line.strip())
        if entry_match and current_section:
            name = entry_match.group(1)
            current_entries.append((i, name))
    
    # Check last section
    if current_section and current_entries:
        errors.extend(check_section(current_section, current_entries))
    
    print("=" * 60)
    print("ALPHABETIZATION CHECK RESULTS")
    print("=" * 60)
    
    if errors:
        print(f"\n❌ Found {len(errors)} alphabetization issues:\n")
        for error in errors[:15]:  # Show first 15
            print(f"  Section: {error['section']}")
            print(f"    Line {error['line']}: '{error['current']}' should come after '{error['next']}'")
            print()
        if len(errors) > 15:
            print(f"  ... and {len(errors) - 15} more issues")
    else:
        print("\n✅ All sections are properly alphabetized!")
    
    print("=" * 60)
    print(f"Total issues: {len(errors)}")
    print("=" * 60)
    
    return len(errors) == 0

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'README.md'
    success = check_alphabetization(filepath)
    sys.exit(0 if success else 1)
