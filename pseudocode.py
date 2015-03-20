##My idea is to write a program to build, from three independent lists of genes associated with vocal-learning, one without duplicates and the sequence of each gene. The lists contain approximately 2,700, 500 and 2,000 genes.

from pandas import DataFrame, read_csv
import pandas as pd

# Import the lists of the publications, they are as supplemental material online.

# Organize the different lists to have the same order of columns and format.
	# Hilliard et al 2012 had more information than I needed, so the processing was a little longer. It was processed in R(document:Organizing_tables.R)
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

get_geneseq("NoDuplicates_final.csv", "Run1", "GeneInfo", species= "taeniopygia_guttata", Rel =78)

# To check for the errors
GeneSeq1 = pd.read_csv("Run1.csv", header = 0)
# from 10724 genes, only 1174 had erros

# To find the gene symbols or IDs without sequences:
No_seq1 = GeneSeq1[GeneSeq1["StableID"] == "No_ID"]
No_seq1["GeneInfo"].to_csv("No_seq1.csv", index=False, header = True)
# Ran the same function again with the genes that I didnt find sequences in the first time. Got another 15 sequences, which indicates that there is a problem with the connection. 
get_geneseq("No_seq1.csv", "Run2", "GeneInfo", species= "taeniopygia_guttata", Rel =78)
#some gene IDs were described in the human genome:
GeneSeq2 = pd.read_csv("Run2.csv", header = 0)
No_seq2 = GeneSeq2[GeneSeq2["StableID"] == "No_ID"]
No_seq2["GeneInfo"].to_csv("No_seq2.csv", index=False, header = True)

get_geneseq("No_seq2.csv", "Run3", "GeneInfo", species = "homo_sapiens", Rel =79) # same function but with the human genome

#only 348 genes have no sequences now

#I removed the items from the column "GeneInfo" that clearly were not genes (17 cases of dates in the format "12-April", were easily removed with regular expressions). GenesIDs starting with "LOC" were removed (using LOC[0-9]*\n in gedit), as their function are not well defined and there is a possibility of being non coding areas. There were 206 LOC genes. 
#I found some problems with the symbols described by Whitney et al 2014. In this table they also put the gene IDs, so had to use  I retrieved them using: 

Whitney = pd.read_csv("Whitney_TableS4.csv", header = 2) # Whitney_TableS4.csv is the table i used to select the gene symbles initially (begining of the code)

GeneSeq3 = pd.read_csv("Run3.csv", header = 0)
No_seq3 = GeneSeq3[GeneSeq3["StableID"] == "No_ID"]
No_seq3["GeneInfo"].to_csv("No_seq3.csv", index=False, header = True)
Symbol = pd.read_csv("No_seq3.csv", header = 0)

XP = []
for i in range(len(Symbol)):
    a = re.search("XP_[A-Z.0-9]*", str(Symbol.loc[i]))
    if a != None:
        XP.append(a.group())

XP_symbols_ID = Whitney["ENSEMBL ID"][Whitney["Symbol"].isin(XP)]
XP_symbols_ID.to_csv("XP_symbols_ID.csv", index=False, header = True)
get_geneseq("XP_symbols_ID.csv", "Run4", "ENSEMBL ID", species= "taeniopygia_guttata", Rel =78)

# I also used the ckicken genome, but it added only 3 sequences to my table
get_geneseq("No_seq3.csv", "Run5", "GeneInfo", species = "gallus_gallus", Rel =79)

# All ran okay. Now I need to concatenate the results from the different runs
def get_finaltable (imput_list_tables):
    Final_table = pd.DataFrame()
    for file in allruns:
        read = pd.read_csv(file, header = 0)
        Seq = read[read["StableID"] != "No_ID"]
        Final_table = Final_table.append(Seq)
    seq = Final_table[["StableID", "DNAseq"]]
    seq.to_csv("Sequences.csv", index=False, header = True)
    get_uniqueGenes ("Sequences.csv", "Final_table", "StableID")
    print "Done!"

allruns = glob.glob("Run[1-5].csv")
get_finaltable (allruns, "Final_table")
#output: Only one table was analyzed. Initial length the table: 11633. Unique genes in the list: 9849. "Done!"

# Only 46 genes remained without sequences (less than 1%). One example of a gene that didnt work is "ZGC:113518", they call it a synonymous name, and I did not find a way to get the gene ID or symbol from it. Also, IDs like "ENSGALT00000005719" are of transcripts, I also did not find a way to solve those (however I am sure I will find after some more digging). Others could not be found even searching manually in the website, which I think are typos or names not related with genes (wrongly selected by my code).

#To represent graphically my data, I


