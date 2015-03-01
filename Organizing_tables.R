#clear memory
rm(list = ls())
# set working directory
setwd("/home/gabriela/Dropbox/Documents/Doutorado/EEB177_234/Final-Project")

## Table from Hilliard et al 2012 - This table has information about genes correlated and non correlated with vocalization, so this script filter only the probes qith genes significantly correlated with singing

# tab <- read.table("http://www.website/data.txt")
tab_hil <- read.table("TableS2_Hilliard_etal2012.csv", header=TRUE, row.names=NULL, sep=",", stringsAsFactors=FALSE, comment.char="") # stringsAsFactors=FALSE is super important because it tells R to read character strings (text) as class "character" rather than class "factor".
head(tab_hil)
length(tab_hil[,1]) # 20104.. right!

# reduce the number of columns to have only information that is useful for me
Subset_tab_hil <- tab_hil[,c(1:5,12,16,39:44,50:53)]
head(Subset_tab_hil) # conlumn names: "probeID","cloneID","sequence","geneSymbol","geneName","percentchange.X","percentchange.V", "tstat.X", "tstat.Xqval", "tstat.V", "tstat.Vqval","Wada et al.", "Wada et al. grouping", "Warren et al. pos selected", "Warren et al. expr time course"
# other usable code for the same purpose: subset[tab_hil, select=c("Wada et al.", "Wada et al. grouping", "Warren et al. pos selected", "Warren et al. expr time course")]
length(Subset_tab_hil[,1])

class(Subset_tab_hil[,10])
## Select only the genes that are regulated by singing.
#singing <- Subset_tab_hil[Subset_tab_hil$q.GS.singing.X < 0.05 & Subset_tab_hil$q.GS.singing.X != "NA",]
#motifs <- Subset_tab_hil[Subset_tab_hil$q.GS.motifs.X < 0.05 & Subset_tab_hil$q.GS.motifs.X != "NA",]
#length(singing[,1]) # 2658 right! -> same number described in the paper
#length(motifs[,1]) # 3706 -> same number described in the paper

Final_table_hil <- Subset_tab_hil[Subset_tab_hil$q.GS.singing.X < 0.05 | Subset_tab_hil$q.GS.motifs.X < 0.05,]
length(Final_table_hil[,1]) # 4161 probes, which I expect to represent 2057 genes regulated by singing
#tail(Final_table_hil)
#head(Final_table_hil)

write.table(Final_table_hil, file ="Probes_vocalization_Hilliardetal2012_extended.csv", sep=",", row.names = FALSE, col.names = TRUE)

Final_table_hil_main <- Final_table_hil[,c("geneSymbol","cloneID")]
head (Final_table_hil_main[1])
colnames(Final_table_hil_main)[1] <- "GeneInfo"

write.table(Final_table_hil_main[1], file ="Probes_vocalization_Hilliardetal2012_GeneInfo.csv", sep=",", row.names = FALSE) # this table will be used to compare with tables from other studies

#232+693+1132=2057
