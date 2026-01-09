#!/usr/bin/env python3
"""
PSS/E Raw File Cleaner

This script reads a PSS/E .raw file and removes invalid branch definitions
where both bus numbers are the same. These invalid entries cause errors when
loading the file into PSS/E, as a branch cannot connect a bus to itself.

Usage:
    python clean_psse_raw.py input.raw output.raw
    python clean_psse_raw.py input.raw  # outputs to input_cleaned.raw
"""

import sys
import os
import re
from pathlib import Path


def is_branch_line(line):
    """
    Determine if a line is a branch definition line.
    
    Branch lines typically start with two integers (bus numbers) separated by comma.
    Example: "143261, 143261,'1 ',...", "  1234,  5678, '1', ..."
    
    Args:
        line: A line from the .raw file
        
    Returns:
        tuple: (is_branch, bus1, bus2) where is_branch is bool,
               bus1 and bus2 are the first two integers if found
    """
    line = line.strip()
    
    # Skip empty lines and comment lines
    # End-of-section markers typically look like "0 /" or "  0  /"
    if not line or re.match(r'^\s*0\s*/', line) or line.startswith('/'):
        return False, None, None
    
    # Try to parse the first two comma-separated values as integers
    parts = line.split(',')
    if len(parts) >= 2:
        try:
            # Extract and clean the first two values
            bus1_str = parts[0].strip()
            bus2_str = parts[1].strip()
            
            # Try to convert to integers
            bus1 = int(bus1_str)
            bus2 = int(bus2_str)
            
            return True, bus1, bus2
        except (ValueError, IndexError):
            # Not a branch line if we can't parse integers
            return False, None, None
    
    return False, None, None


def is_section_header(line):
    """
    Check if a line is a section header in PSS/E format.
    Section headers typically end with data like "/ END OF ..." or similar markers.
    
    Args:
        line: A line from the .raw file
        
    Returns:
        bool: True if the line appears to be a section header
    """
    line = line.strip()
    # Common section markers in PSS/E files
    section_keywords = ['BEGIN', 'END OF', 'CASE IDENTIFICATION', 'BUS DATA', 
                        'LOAD DATA', 'GENERATOR DATA', 'BRANCH DATA', 
                        'TRANSFORMER DATA', 'AREA DATA', 'ZONE DATA']
    
    return any(keyword in line.upper() for keyword in section_keywords)


def clean_raw_file(input_path, output_path):
    """
    Clean a PSS/E .raw file by removing invalid branch definitions.
    
    Invalid branch definitions are lines where the first two bus numbers
    (representing the from-bus and to-bus) are identical, which means
    a branch connecting a bus to itself.
    
    Args:
        input_path: Path to the input .raw file
        output_path: Path to the output cleaned .raw file
        
    Returns:
        tuple: (total_lines, removed_lines) count statistics
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    removed_count = 0
    total_lines = 0
    removed_lines_info = []
    
    with open(input_path, 'r', encoding='utf-8', errors='replace') as infile:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for line_num, line in enumerate(infile, 1):
                total_lines += 1
                
                # Check if this is a branch line with identical bus numbers
                is_branch, bus1, bus2 = is_branch_line(line)
                
                if is_branch and bus1 == bus2:
                    # This is an invalid branch - skip it
                    removed_count += 1
                    removed_lines_info.append((line_num, bus1, line.strip()))
                    print(f"Removing invalid branch at line {line_num}: "
                          f"Bus {bus1} connected to itself")
                else:
                    # Write the line to output
                    outfile.write(line)
    
    return total_lines, removed_count, removed_lines_info


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python clean_psse_raw.py <input_file> [output_file]")
        print("\nExample:")
        print("  python clean_psse_raw.py input.raw output.raw")
        print("  python clean_psse_raw.py input.raw  # outputs to input_cleaned.raw")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Determine output file
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Default output: add '_cleaned' before extension
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_cleaned{input_path.suffix}")
    
    print(f"PSS/E Raw File Cleaner")
    print(f"=" * 60)
    print(f"Input file:  {input_file}")
    print(f"Output file: {output_file}")
    print(f"=" * 60)
    
    try:
        total_lines, removed_count, removed_info = clean_raw_file(input_file, output_file)
        
        print(f"\nProcessing complete!")
        print(f"Total lines processed: {total_lines}")
        print(f"Invalid branches removed: {removed_count}")
        
        if removed_count > 0:
            print(f"\nRemoved {removed_count} invalid branch(es):")
            for line_num, bus, line_text in removed_info:
                print(f"  Line {line_num}: Bus {bus} -> {bus}")
        else:
            print("\nNo invalid branches found. File is clean!")
        
        print(f"\nCleaned file saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
