# Use MED to identify nodes within the 16S rRNA gene sequence data
# This code uses a clustering technique described in: https://www.nature.com/articles/ismej2014195
# Code modified from Joe Vineis (https://github.com/jvineis/med-anvio-workshop/wiki/MED--and-Phyloseq)

# Merge sequences together
cat *MERGED-MAX-MISMATCH-3 > sequences-to-oligotype.fa
o-pad-with-gaps sequences-to-oligotype.fa -o sequences-to-oligotype-padded.fa

# Run MED (where M is the minimum substantive abundance of an oligotype)
# This could take a while depending on the number of reads
decompose sequences-to-oligotype-padded.fa -M 20 


