from pandas import DataFrame, read_csv
import pandas as pd

# This function eliminates duplicates within each file and among files, having as output one file with unique genes (Symbol or ID, it depends on what was published). Also, it shows the initial number of genes in each list and the final number after removal of duplicates and NAs, as well as the final number of unique genes from all lists. 
# It has 3 arguments: alltables (one string with the name of the file if working with one table, or a list of file names when working with several tables), name_output_table (a string with the prefered name to the output file), name_column (name of the column with information about the gene).

def get_uniqueGenes (alltables, name_output_table, name_column):
    Final_list = pd.DataFrame() # creates an empty Dataframe
    Number_genes_per_table = []
    Initial_size = []
    if type(alltables) == str: # if only one table was used as input
        table = pd.read_csv(alltables, header = 0)
        Final_list_noduplicates = table.drop_duplicates([name_column]).dropna()
        print "Only one table was analyzed. Initial length the table: " + str(len(table[name_column])) + ". Unique genes in the list: " + str(len(Final_list_noduplicates)) + "."

    if type(alltables) != str: # if several tables are being compared and analyzed
        for table in alltables:
            table = pd.read_csv(table, header = 0)
            Initial_size.append(len(table[name_column]))
            SingleGenes = table.drop_duplicates([name_column]).dropna() # the output is all your table without duplicates
            Number_genes_per_table.append(len(SingleGenes))
            Final_list = Final_list.append(SingleGenes)
        Final_list_noduplicates = Final_list.drop_duplicates([name_column]) # to exclude genes repeated among lists    
        print "Analyzed tables: "+ str(alltables) +". Initial lengths of tables: " + str(Initial_size) + ". Unique genes per list: " + str(Number_genes_per_table) + ". Size of the final list is: "+ str(len(Final_list_noduplicates)) + "."

    Final_list_noduplicates.to_csv('{}.csv'.format(name_output_table), index = False) # index=True would write the name of the rows
    

