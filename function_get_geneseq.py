from cogent.db.ensembl import Genome
Zebra = Genome(Species='Zebra finch', Release=78, account=None) # information about the release searched in the ensemble website
#Human = Genome(Species='Human', Release=67, account=None)

# information about the curl is in http://rest.ensembl.org/documentation/info/xref_external

import pexpect
import re
from pandas import DataFrame, read_csv
import pandas as pd
import sys
#import StringIO
#Hilliard = pd.read_csv("Hilliard_Noduplicates.csv", header = 0)
Table1 = pd.read_csv("Test.csv", header = 0)

#This function is working for "Teste.csv", but I still need to change for some specific cases (when the author put the geneID instead og the GeneSymbol)

def get_geneseq (input_table, name_output_table):
    Seq = []
    StableID = []
    for GeneSymbol in input_table["geneSymbol"]:
        GeneInfo = pexpect.run("curl 'http://rest.ensembl.org/xrefs/symbol/taeniopygia_guttata/{}?' -H 'Content-type:application/json'".format(GeneSymbol))
        ID_re = re.search('.id.:.([\w\d]*).', GeneInfo)
        geneID = ID_re.group(1)
        Gene = Zebra.getGeneByStableId(StableId = geneID)
        Seq.append(str(Gene.Seq))
        StableID.append(str(Gene.StableId))
    input_table['StableID'] = StableID
    input_table['DNAseq'] = Seq
    input_table.to_csv('{}.csv'.format(name_output_table), index=False, header=True)
    print ("Done!")

get_geneseq(Table1, "Table1_final")
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



