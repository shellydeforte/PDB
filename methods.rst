Objectives and Methods
======================

This is a bioinformatics implementation of the method outlined in the paper *Resolving
the Ambiguity: Making Sense of Intrinsic Disorder when PDB Files
Disagree* (submitted). The purpose of this method is to classify missing
regions in PDB files by the pattern of disorder among multiple missing
regions. If you find this method useful, please cite the corresponding paper.

The method first obtains the required data files from the PDB, which
are:

+-----------------------------+--------------------------------------------------------------------------------------+
| Filename                    | URL                                                                                  |
+=============================+======================================================================================+
| *pdb\_chain\_uniprot.tsv*   | https://www.ebi.ac.uk/pdbe/docs/sifts/quick.html                                     |
+-----------------------------+--------------------------------------------------------------------------------------+
| *ss\_dis.txt*               | http://www.rcsb.org/pdb/static.do?p=download/http/index.html                         |
+-----------------------------+--------------------------------------------------------------------------------------+
| *pdb\_entry\_type.txt*      | http://www.rcsb.org/pdb/static.do?p=general\_information/about\_pdb/summaries.html   |
+-----------------------------+--------------------------------------------------------------------------------------+

Additionally, this script will download the necessary UniProt files for
file comparison.

These files are manipulated using the Pandas package.

The following filtering steps are performed:

1. Remove any rows where the PDB ID isn't in the xray list
2. Remove any rows where the PDB ID is in the obs list
3. Remove any rows with bad indexes in *pdb\_chain\_uniprot.tsv*
4. Remove any rows where the length of the pdb interval (the portion of
   the chain that corresponds to a specific UniProt entry) is <= 3
   residues
5. Remove any rows for pdb\_chains not in *ss\_dis*
6. Remove any entries that are not a 100% sequence match with the
   corresponding section of the UniProt entry

Finally, this method creates two tab delimited files which may be loaded
using Pandas for further analysis.

*pdb\_df.tsv* and *pdb\_df.pkl*

*uni\_df.tsv* and *pdb\_df.pkl*

The tsv (tab-separated) files and the pkl (pickle) files are the same,
however when using Pandas, you need to use the pkl files so they are
read correctly.

pdb\_df has the following fields:

-  PDB\_CHAIN: The PDB ID, followed by an underscore, and then the chain
   ID
-  SEC\_STRUCT: A composite of the structural elements for that PDB
   chain. See the paper associated with this project for the secondary
   structure key.
-  SP\_PRIMARY: The UniProt ID

uni\_df has the following fields:

-  SP\_PRIMARY: The UniProt ID
-  STRUCT: A composite structure between all PDB chains. See the paper
   associated with this project for the secondary structure key.
-  MISSING: This is a list of that has the type of missing region, and
   the interval of that region.

Data Sources and Dates
======================

This is the information for the data used in the project.

As of July 9, 2015 (PDB release July 9, 2015), according to
pdb\_entry\_type.txt, there were 96,525 pdb entries of proteins, protein
complexes, or protein-nucleic acid complexes solved by x-ray
diffraction. Note this was 40 less than that shown in the PDB Current
Holdings Breakdown, however my suspicion is that this is because the
current holdings data was slightly lagging.

Of this group, 89,523 were available in ss\_dis.txt, which has a missing
residue fraction of 0.057.

Because we were concerned only with missing residues, it was not
necessary to parse the pdb files directly, and instead we used the
following files:

+-----------------------------+--------------------------------------------------------------------------------------+--------------------+
| Filename                    | URL                                                                                  | Date of Download   |
+=============================+======================================================================================+====================+
| *pdb\_chain\_uniprot.tsv*   | https://www.ebi.ac.uk/pdbe/docs/sifts/quick.html                                     | 07/04/15           |
+-----------------------------+--------------------------------------------------------------------------------------+--------------------+
| *ss\_dis.txt*               | http://www.rcsb.org/pdb/static.do?p=download/http/index.html                         | 07/08/15           |
+-----------------------------+--------------------------------------------------------------------------------------+--------------------+
| *pdb\_entry\_type.txt*      | http://www.rcsb.org/pdb/static.do?p=general\_information/about\_pdb/summaries.html   | 07/09/15           |
+-----------------------------+--------------------------------------------------------------------------------------+--------------------+
