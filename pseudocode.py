##My idea is to write a program to build, from three independent lists of genes associated with vocal-learning, one without duplicates and the sequence of each gene. The lists contain approximately 2,700, 500 and 2,000 genes.

from pandas import DataFrame, read_csv
import pandas as pd

# Import the lists of the publications, they are as supplemental material online.

# Organize the different lists to have the same order of columns and format.
	# Hilliard et al 2012 had more information than I needed, so the processing was a little longer. It was processed in R(document:Organizing_tables.R)
Hilliard = pd.read_csv("Probes_vocalization_Hilliardetal2012_GeneInfo.csv", header = None)
	# Zhang et al 2014 has two tables of interest (one with 227 and the other 278 genes) that have different organization. So I had to organize it:
Zhang1 = pd.read_csv("Zhang-Table_S28.txt", delim_whitespace=True, header = 1)
Zhang1["GeneSymbol"].to_csv("Zhang1_GeneSymbol.csv", index=False, header = None)
	# The other table was a giant mess, so I used regular expressions to select the information I was interested (geneID). In shell I ran: grep -o -E "ENST[A-Z 0-9]*" Zhang-Table_S34.txt > ZhangS34_GeneID.csv
Zhang2 = pd.read_csv("ZhangS34_GeneID.csv", header = None)
len(Zhang2) # 331, that is the same described in the paper :)
	# Whitney et al 2014
Whitney = pd.read_csv("Whitney_TableS4.csv", header = 2)
Whitney["Symbol"].to_csv("Whitney_geneSymbol.csv", index=False, header = None)

## to eliminate duplicates within each file and make only one file
run function_get_uniqueGenes.py

import glob
alltables = glob.glob("*.csv")
get_uniqueGenes (alltables, "First_version")
get_uniqueGenes ("First_version.csv", "NoDuplicates_final")

# 2057 single genes! As expected :)
a = Whitney["Symbol"]
b = a[a != "ASB18"]
## Get the whole sequence of genes and gene stableID from ensembl.org
# Ensembl makes their data available via MySQL servers, that can be accessed by cogent.db.ensembl module in PyCogent. PyCogent is a software library for genomic biology) that uses Python language. This program instalation have several requirements, including for querying databases, the script used to install this and other softwares is in the document "Pycogent_install.sh".
from cogent.db.ensembl import Species # Species is a module in cogent.db.ensembl that let us know which species have a genome available to be used (its possible to add species to this list or to change the names if you want). http://pycogent.org/examples/query_ensembl.html

print Species # great! Zebra finch is included! (Common Name:Zebra finch, Species Name: Taeniopygia guttata, Ensembl Database Prefix: taeniopygia_guttata)

# To get the sequences, I made the get_geneseq function

run function_get_geneseq.py


#### Just some notes for myself here
#join the lists
a = [list1, list2, list3]
concatenated = pandas.concat(a)

# to check if there are duplicates into the lists
concatenated.duplicated([3])
#or list1.groupby(list1[1]).agg([len])

final.to_csv('Noduplicates.csv', index=False, header=False) # to write a file with the final number of genes # names=['x','y']

# Check data type of columns: list1[1].dtype

