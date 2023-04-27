#!/usr/bin/env python3
"""Add a column to a .tsv file.

Given a .tsv version of a .vcf as well as a .bed, add a column to the 
.tsv based on the info. in the .bed.  The new column should have the row 
number in the .bed to which the given row in the .tsv corresponds.  This 
is needed so that the .tsv will contain the information on the nodes in 
the graph. If we didn't do this, we wouldn't know which rows in the .tsv 
correspond to which nodes in the graph.
"""

import argparse

def main():
    user_args = get_user_args()
    loci_to_node = get_loci_to_node_dict(vcf=user_args.vcf)
    
    add_nodes_to_tsv(loci_to_node=loci_to_node,
                     tsv=user_args.tsv,
                     out=user_args.o)
    return None

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


def get_loci_to_node_dict(vcf):
    """Get a dictionary whose keys are loci

    and whose values are node_ids.
    """
    loci_to_node = dict()
    node_id = -1

    with open(file=vcf, mode="r") as vcf:
        for line in vcf:
            # If a line is a formatted a certain way,
            # then we can recognize it as a tabix region header.
            # We need to increase
            # the node_id because whatever we find next
            # is another region that we need.
            if line[0] == "#" and line[1] != "#" and ("\t" not in line):
                node_id += 1
                # This is the section for genomic loci 
                # corresponding to the first region.
                # Skip the header part.
 
            # Check that the section is not empty.
            elif not line.startswith("#") and ("\t" in line):
                # line now has the info. we need in it.
                # Get the first two fields
                loci = "\t".join(line.split(sep="\t", maxsplit=2)[0:2])
                loci_to_node[loci] = node_id
    
    return loci_to_node


def add_nodes_to_tsv(loci_to_node, tsv, out):  
    # Loop through the .tsv, figure out what's in there,
    # and then write to out accordingly.
    with open(file=tsv, mode="r") as tsv:
        with open(file=out, mode="w") as out:
            tsv_first_line = tsv.readline()
            # Prepend "node_id\t" to the first line.
            new_tsv_first_line = "\t".join(["node_id", tsv_first_line])
            # Write the line to the output file.
            out.write(new_tsv_first_line)
            # Iterate through lines, using loci_to_node for lookups.
            for tsv_line in tsv:
                # Get the first two fields
                locus = "\t".join(tsv_line.split(sep="\t", maxsplit=2)[0:2])

                node_id = loci_to_node[locus] 
                # Prepend node_id to the line.
                # Write the line to the output file.
                out.writelines([node_id, "\t", tsv_line])
                  
    return None


###############################################################################
# if this module is being run directly and not imported
if __name__ == "__main__":
    # Call the function main.
    main()