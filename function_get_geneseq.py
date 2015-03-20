from cogent.db.ensembl import Genome
import pexpect
import re
from pandas import DataFrame, read_csv
import pandas as pd
import sys

# This function uses the database of Ensemble via MySQL server. From information about gene symbol or gene ID, it can find the gene sequence for a large dataset. It can easily be modified to find other information about the gene, as description or gene type. It uses three arguments: input_table (a string of the name of the file to be analyzed), name_output_table (a string of the prefered name for the output file), name_column (a string of the column name where there is information about Ensemble gene symbol or gene ID), head (0 if the table has header, False if it does not, default = 0), Rel (release of the genome), species (the name of the species in which the gene information will be found, it needs to be a name accepted by Ensembl, example taeniopygia_guttata).

# information about the curl is in http://rest.ensembl.org/documentation/info/xref_external


def get_geneseq (input_table, name_output_table, name_column, species, Rel, head = 0):
    table = pd.read_csv(input_table, header = head)
    genome = Genome(Species='{}'.format(species), Release= Rel, account=None)#information about the release searched in the ensemble website
    Seq = []
    StableID = []
    for GeneSymbol in table[name_column]:
        if re.search("ENS[A-Z 0-9]*", GeneSymbol) != None:
            Gene = genome.getGeneByStableId(StableId = GeneSymbol)
            if str(Gene) == 'None':
                Seq.append("No_seq")
                StableID.append("No_ID")
            else:
                Seq.append(str(Gene.Seq))
                StableID.append(str(Gene.StableId))

        if re.search("ENS[A-Z 0-9]*", GeneSymbol) == None:
            GeneralInfo = pexpect.run("curl 'http://rest.ensembl.org/xrefs/symbol/{}/{}?' -H 'Content-type:application/json'".format(species, GeneSymbol))
            if str(GeneralInfo) != '[]':
                ID_re = re.search('.id.:.([\w\d]*).', GeneralInfo)
                if ID_re == None:
                    Seq.append("No_seq")
                    StableID.append("No_ID")
                else:
                    geneID = ID_re.group(1)
                    Gene = genome.getGeneByStableId(StableId = geneID)
                    Seq.append(str(Gene.Seq))
                    StableID.append(str(Gene.StableId))
            else:
                Seq.append("No_seq")
                StableID.append("No_ID")

    table['StableID'] = StableID
    table['DNAseq'] = Seq
    table.to_csv('{}.csv'.format(name_output_table), index=False, header=True)
    print ("Done!")

