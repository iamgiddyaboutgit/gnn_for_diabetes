#!/usr/bin/env python3
"""Add a column to a .tsv file.

Given a .tsv version of a .vcf as well as a .bed, add a column to the 
.tsv based on the info. in the .bed.  The new column should have the row 
number in the .bed to which the given row in the .tsv corresponds.  This 
is needed so that the .tsv will contain the information on the nodes in 
the graph. If we didn't do this, we wouldn't know which rows in the .tsv 
correspond to which nodes in the graph.
"""

import sys
import argparse

def main():
    user_args = get_user_args()
    # Find the first occurrence of a line in the .vcf
    # that starts with a # and doesn't contain any tabs.
    
    # Get the first two fields in following lines until
    # we reach another line that starts with # or the
    # end of the file.

def get_user_args() -> argparse.Namespace:
    """Get arguments from the command line and validate them."""
    parser = argparse.ArgumentParser(description = "Add a column to a .tsv file.")
    # Optional arguments are prefixed by single or double dashes.
    # The remaining arguments are positional.
    parser.add_argument("--tsv", required = True,
        help=".tsv file to modify")
    parser.add_argument("--vcf", required = True,
        help="an uncompressed .vcf file that has already been grouped by the regions in a sorted .bed file using tabix")
    parser.add_argument("-o", required=True,
        help="Output path for new .tsv file")
    args = parser.parse_args()

    return args

###############################################################################
# if this module is being run directly and not imported
if __name__ == "__main__":
    # Call the function main.
    main()