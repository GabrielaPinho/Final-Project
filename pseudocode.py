##My idea is to write a program to build, from three independent lists of genes associated with vocal-learning, one without duplicates. The lists contain approximately 2,700, 500 and 2,000 genes. My steps will be.

from pandas import DataFrame, read_csv
import pandas as pd

# Import the lists of the publications, they are as supplemental material online.

# Organize the different lists to have the same order of columns and format.
# Hilliard et al 2012 processed in R (document:Organizing_tables.R)
# eliminate duplicates within each file
Hilliard = pd.read_csv("Probes_vocalization_Hilliardetal2012_GeneInfo.csv", header = 0)
Hilliard.duplicated(["geneSymbol"]) # check if there are duplicates
SingleGenes = Hilliard.drop_duplicates(["geneSymbol"]) # the output is all your table without duplicates
len(SingleGenes)# 2057 single genes! As expected :) 
SingleGenes.to_csv('Hilliard_Noduplicates.csv', index=False, header=True)



## Get the whole sequence of genes and gene names from ensembl.org
# Ensembl makes their data available via MySQL servers, that can be accessed by cogent.db.ensembl module in PyCogent. PyCogent is a software library for genomic biology) that uses Python language. This program instalation have several requirements, including for querying databases, the script used to install this and other softwares is in the document "Pycogent_install.sh".

######
import numpy #python module used for speeding up matrix computations
#####


## Join the lists and produce one final document with unique genes.

list1 = pd.read_csv("code.csv", header = None) # importing the 3 lists with consistent gene names
list2 = pd.read_csv("novo.csv", header = None)
list3 = pd.read_csv("xxx.csv", header = None)

#join the lists
a = [list1, list2, list3]
concatenated = pandas.concat(a)

# to check if there are duplicates into the lists
concatenated.duplicated([3])
#or list1.groupby(list1[1]).agg([len])

#remove duplicates
final = concatenated.drop_duplicates([3])

final.to_csv('Noduplicates.csv', index=False, header=False) # to write a file with the final number of genes # names=['x','y']

# Check data type of columns: list1[1].dtype

