from pandas import DataFrame, read_csv
import pandas as pd

def get_uniqueGenes (alltables, name_output_table):
    Final_list = open('{}.csv'.format(name_output_table), "w")
    Number_genes_per_table = []
    Initial_size = []

    for table in alltables:
        table = pd.read_csv(table, header = None)
        Initial_size.append(len(table))
        SingleGenes = table.drop_duplicates([0]) # the output is all your table without duplicates
        NoNA = SingleGenes.dropna()
        Number_genes_per_table.append(len(NoNA))
    for line in NoNA:
        Final_list.write(str(line)) #this line is still not working
        Final_list.close()
    print "Analyzed tables: "+ str(alltables) +". Initial lengths of tables: " + str(Initial_size) + ". Unique genes per list: " + str(Number_genes_per_table)

