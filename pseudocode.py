##My idea is to write a program to build, from three independent lists of genes associated with vocal-learning, one without duplicates. The lists contain approximately 2,700, 500 and 2,000 genes. My steps will be.

from pandas import DataFrame, read_csv
import pandas as pd

# Import the lists of the publications, they are as supplemental material online. -> This is giving me more work than I imagine, I still dont have all the lists

#I will have to organize the different lists to have the same order of columns and format. I probably will use Regular expressions in sheel ("grep") to do this.

#Because people give different names to genes, I will have to blast each gene and replace the name given by the authors for the names in GenBank
# in the terminal: 
sudo apt-get install ncbi-blast+
#to search genbank for a sequence, but for only a single species:
blastn -db nt -query nt.fsa -entrez_query "Taeniopygia guttata[Organism]" -out results.out -remote


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

############## I first tried to make one function to compare and produce one list.. but not very successful.

def function (list1,list2)
final = []
for row1 in list1[1]:
	for row2 in list2[1]:
		if row1 == row2:
			print("a")
			break
		else:
			final.append(row2)
			print("b")
	final.append(row1)
return final

# to sort: .sort(['coluna'], ascending=False)


