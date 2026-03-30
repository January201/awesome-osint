#!/usr/bin/env python3
"""
Remove trailing whitespace from all lines in README.md
"""

def remove_trailing_whitespace(filepath, output_path=None):
    if output_path is None:
        output_path = filepath
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Count before
    lines_with_whitespace = sum(1 for line in lines if line.rstrip() != line.rstrip('\n').rstrip())
    
    # Remove trailing whitespace
    trimmed_lines = [line.rstrip() + '\n' if line.endswith('\n') else line.rstrip() for line in lines]
    
    # Count after
    lines_with_whitespace_after = sum(1 for line in trimmed_lines if line.rstrip() != line.rstrip('\n').rstrip())
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(trimmed_lines)
    
    print(f"Removed trailing whitespace:")
    print(f"  Before: {lines_with_whitespace} lines with trailing whitespace")
    print(f"  After: {lines_with_whitespace_after} lines with trailing whitespace")
    print(f"  Fixed: {lines_with_whitespace - lines_with_whitespace_after} lines")
    
    return lines_with_whitespace - lines_with_whitespace_after

if __name__ == '__main__':
    remove_trailing_whitespace('/workspace/README.md')
