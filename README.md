# power-systems

A collection of utilities for working with power systems data and files.

## PSS/E Raw File Cleaner

### Overview

The `clean_psse_raw.py` script reads a PSS/E `.raw` file and removes invalid branch definitions where both bus numbers are the same. These invalid entries cause errors when loading the file into PSS/E, as a branch cannot connect a bus to itself.

### Problem

PSS/E `.raw` files sometimes contain invalid branch definitions where the from-bus and to-bus are identical, such as:
```
143261, 143261, '1 ', 0.00150, 0.01500, 0.00000, 50.0, 50.0, 50.0
```

These lines cause errors when loading the file into PSS/E because a branch cannot connect a bus to itself.

### Solution

The script scans through the `.raw` file line by line, identifies branch definitions where the first two comma-separated values (the bus numbers) are identical, and removes those lines while preserving all other content.

### Usage

```bash
# Basic usage - specify input and output files
python clean_psse_raw.py input.raw output.raw

# Automatic output naming - creates input_cleaned.raw
python clean_psse_raw.py input.raw

# Show help
python clean_psse_raw.py
```

### Example

Given an input file `test_sample.raw`:
```
0, 100.00, 33, 0, 0, 60.00     / PSS/E-33 RAW
...
Branch Data Section
1, 2, '1 ', 0.00100, 0.01000, 0.00000, 100.0, 100.0, 100.0
143261, 143261, '1 ', 0.00150, 0.01500, 0.00000, 50.0, 50.0, 50.0
3, 1, '1 ', 0.00300, 0.03000, 0.00000, 100.0, 100.0, 100.0
143262, 143262, '2 ', 0.00250, 0.02500, 0.00000, 75.0, 75.0, 75.0
0 / END OF BRANCH DATA
```

Running the script:
```bash
python clean_psse_raw.py test_sample.raw
```

Output:
```
PSS/E Raw File Cleaner
============================================================
Input file:  test_sample.raw
Output file: test_sample_cleaned.raw
============================================================
Removing invalid branch at line 13: Bus 143261 connected to itself
Removing invalid branch at line 15: Bus 143262 connected to itself

Processing complete!
Total lines processed: 16
Invalid branches removed: 2

Removed 2 invalid branch(es):
  Line 13: Bus 143261 -> 143261
  Line 15: Bus 143262 -> 143262

Cleaned file saved to: test_sample_cleaned.raw
```

The cleaned file will have the invalid branch lines removed while preserving all other content.

### Features

- ✅ Detects and removes invalid branch definitions (same from-bus and to-bus)
- ✅ Preserves all other file content
- ✅ Handles large files with multiple invalid entries
- ✅ Provides detailed reporting of removed lines
- ✅ Configurable input/output file paths
- ✅ Automatic output file naming
- ✅ Clear error messages and usage instructions

### Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

### Testing

Test files are included in the repository:
- `test_sample.raw` - Contains invalid branch definitions for testing
- `test_clean.raw` - A clean file with no invalid branches

Run the script on the test files to verify functionality:
```bash
python clean_psse_raw.py test_sample.raw
python clean_psse_raw.py test_clean.raw
```