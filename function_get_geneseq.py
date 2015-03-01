from cogent.db.ensembl import Genome
import pexpect
import re
from pandas import DataFrame, read_csv
import pandas as pd
import sys

# This function uses the database of Ensemble via MySQL server. From information about gene symbol or gene ID, it can find the gene sequence for a large dataset. It can easily be modified to find other information about the gene, as description or gene type. It uses three arguments: input_table (a string of the name of the file to be analyzed), name_output_table (a string of the prefered name for the output file), name_column (a string of the column name where there is information about Ensemble gene symbol or gene ID), head (0 if the table has header, False if it does not, default = 0), Rel (release of the genome).

# information about the curl is in http://rest.ensembl.org/documentation/info/xref_external


def get_geneseq (input_table, name_output_table, name_column, head = 0, Rel):
    table = pd.read_csv(input_table, header = head)
    genome = Genome(Species='Zebra finch', Release= Rel, account=None)#information about the release searched in the ensemble website
    Seq = []
    StableID = []
    for GeneSymbol in table[name_column]:
        if re.search("ENST[A-Z 0-9]*", GeneSymbol) != None:
            Gene = genome.getGeneByStableId(StableId = GeneSymbol)
            if str(Gene) == 'None':
                Seq.append("error")
                StableID.append("error")
            else:
                Seq.append(str(Gene.Seq))
                StableID.append(str(Gene.StableId))

        if re.search("ENST[A-Z 0-9]*", GeneSymbol) == None:
            GeneralInfo = pexpect.run("curl 'http://rest.ensembl.org/xrefs/symbol/taeniopygia_guttata/{}?' -H 'Content-type:application/json'".format(GeneSymbol))
            if str(GeneralInfo) != '[]':
                ID_re = re.search('.id.:.([\w\d]*).', GeneralInfo)
                geneID = ID_re.group(1)
                Gene = genome.getGeneByStableId(StableId = geneID)
                Seq.append(str(Gene.Seq))
                StableID.append(str(Gene.StableId))
            else:
                Seq.append("error")
                StableID.append("error")

    input_table['StableID'] = StableID
    input_table['DNAseq'] = Seq
    input_table.to_csv('{}.csv'.format(name_output_table), index=False, header=True)
    print ("Done!")


#### My notes... not important to you :)

#            if str(GeneralInfo) == '{"error":"page not found. Please check your uri and refer to our documentation http://rest.ensembl.org/"}'
#                Seq.append(str(GeneralInfo))
#                StableID.append("error")


#Human = Genome(Species='Human', Release=67, account=None)
#Hilliard = pd.read_csv("Hilliard_Noduplicates.csv", header = 0)
#Table1 = pd.read_csv("Test.csv", header = 0)

#get_geneseq(Table1, "Table1_final1")
#input_table = Hilliard
#name_output_table = "Hilliard_final"

#out: [{u'type': u'gene', u'id': u'ENSG00000139618'}, {u'type': u'gene', u'id': u'LRG_293'}]
#GeneSymbol = "NTRK2"


#ntrk2 = Zebra.getGeneByStableId(StableId='ENSTGUG00000003077')
#ntrk2 = Human.getGeneByStableId(StableId= 'ENSG00000148053')
#ntrk2.Seq

####
#genes = Zebra.getGenesMatching(Symbol='NTRK2') # this is a search for a gene based on the genesymbol (returns a matching object)
#genesH = Human.getGenesMatching(Symbol='NTRK2')


#genes.Symbol
#for gene in genes: # it let you interate in the 
#     if gene.Symbol.lower() == 'ntrk2':
#         break



