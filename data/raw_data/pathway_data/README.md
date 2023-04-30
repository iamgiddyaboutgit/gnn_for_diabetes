The file ```Human.MitoCarta3.0.xls``` was downloaded from the [Broad Institute](https://www.broadinstitute.org/mitocarta/mitocarta30-inventory-mammalian-mitochondrial-proteins-and-pathways) on 2023-04-28. From Sheet A Human MitoCarta3.0, all of the listed genes were selected for further analysis.

```GenomeLoci_MITOMAP_Foswiki.csv``` was downloaded from [MitoMap](https://www.mitomap.org/foswiki/bin/view/MITOMAP/GenomeLoci) on 2023-04-28.  It contains all of the Mitochondrial DNA Function Locations recorded in MitoMap. These genetic loci were added to the list to analyze.

The file ```genomic_loci_list_before_interactions.csv``` contains all of the above loci that were selected.

The results of the Intact search are contained in the file 2023-04-29-01-16_intact.txt.

The genes that failed to map to the IntAct database are listed in the file 2023-04-29-01-16_intact_could_not_handle.csv.  These genes were queried against the [String](https://string-db.org/) database.  All of these genes were able to map against the String database as shown in file string_mapping.tsv.

For using String, the full String network was chosen.  However, interactions were filtered with a required score of low confidence (0.15) and an FDR stringency of lenient (25%). The meaning of the network edges was set to confidence.  All active interaction sources were used.  The results of the String query are in the file string_interactions_for_genes_intact_could_not_handle.tsv.
