##My idea is to write a program to build, from three independent lists of genes associated with vocal-learning, one without duplicates and the sequence of each gene. The lists contain approximately 2,700, 500 and 2,000 genes.

from pandas import DataFrame, read_csv
import pandas as pd

# Import the lists of the publications, they are as supplemental material online.

# Organize the different lists to have the same order of columns and format.
	# Hilliard et al 2012 had more information than I needed, so the processing was a little longer. It was processed in R(document:Organizing_tables.R)
Hilliard = pd.read_csv("Probes_vocalization_Hilliardetal2012_GeneInfo.csv", header = 0)
	# Zhang et al 2014 has two tables of interest (one with 227 and the other 278 genes) that have different organization. So I had to organize it:
Zhang1 = pd.read_csv("Zhang-Table_S28.txt", delim_whitespace=True, header = 1)
Zhang1 = Zhang1.rename(columns={"GeneSymbol": "GeneInfo"})
Zhang1["GeneInfo"].to_csv("Zhang1_GeneInfo.csv", index=False, header = True)
	# The other table was a giant mess, so I used regular expressions to select the information I was interested (geneID). In shell I ran: grep -o -E "ENST[A-Z 0-9]*" Zhang-Table_S34.txt > ZhangS34_GeneID.csv
Zhang2 = pd.read_csv("ZhangS34_GeneID.csv", names = ["GeneInfo"])
Zhang2.to_csv("Zhang2_GeneInfo.csv", index=False, header = True)
len(Zhang2) # 331, that is the same described in the paper :)
	# Whitney et al 2014
Whitney = pd.read_csv("Whitney_TableS4.csv", header = 2)
Whitney = Whitney.rename(columns={"Symbol": "GeneInfo"})
Whitney["GeneInfo"].to_csv("Whitney_GeneInfo.csv", index=False, header = True)

## to eliminate duplicates within each file and make only one file
run function_get_uniqueGenes.py

import glob
alltables = glob.glob("*.csv")
get_uniqueGenes (alltables, "NoDuplicates_final", "GeneInfo")
# output: Analyzed tables: ['Probes_vocalization_Hilliardetal2012_GeneInfo.csv', 'Zhang1_GeneInfo.csv', 'Whitney_GeneInfo.csv', 'Zhang2_GeneInfo.csv']. Initial lengths of tables: [4161, 227, 24498, 331]. Unique genes per list: [2056, 227, 10253, 284]. Size of the final list is: 10726.

## Get the whole sequence of genes and gene stableID from ensembl.org
# Ensembl makes their data available via MySQL servers, that can be accessed by cogent.db.ensembl module in PyCogent. PyCogent is a software library for genomic biology) that uses Python language. This program's instalation have several requirements, and some details for querying databases. The script used to install this and other softwares is in the document "Pycogent_install.sh".

# Species is a module in cogent.db.ensembl that let us know which species have a genome available to be used (its possible to add species to this list or to change the names if you want). http://pycogent.org/examples/query_ensembl.html
from cogent.db.ensembl import Species 
print Species # great! Zebra finch is included! (Common Name:Zebra finch, Species Name: Taeniopygia guttata, Ensembl Database Prefix: taeniopygia_guttata)

## To get the gene sequences, gene symbol and gene ID, I developed the function get_geneseq
run function_get_geneseq.py
# some gene IDs came with the prefix "SYM", I removed it with regular expressions using the find/replace in gedit (find:SYM(ENST[A-Z 0-9]*) replace: \1)

#Noduplicates = pd.read_csv("NoDuplicates_final.csv", header = 0)
get_geneseq("NoDuplicates_final.csv", "GeneSeq_final", "GeneInfo", Rel =78)

# To check for the errors
GeneSeq_final = pd.read_csv("GeneSeq_final.csv", header = 0)
len(GeneSeq_final[] == "error")


#### Just some notes for myself here
#join the lists
a = [list1, list2, list3]
concatenated = pandas.concat(a)

# to check if there are duplicates into the lists
concatenated.duplicated([3])
#or list1.groupby(list1[1]).agg([len])

final.to_csv('Noduplicates.csv', index=False, header=False) # to write a file with the final number of genes # names=['x','y']

# Check data type of columns: list1[1].dtype

