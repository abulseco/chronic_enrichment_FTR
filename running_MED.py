# Use MED to identify nodes within the 16S rRNA gene sequence data
# This code uses a clustering technique described in: https://www.nature.com/articles/ismej2014195
# Code modified from Joe Vineis (https://github.com/jvineis/med-anvio-workshop/wiki/MED--and-Phyloseq)

# Merge sequences together
cat *MERGED-MAX-MISMATCH-3 > sequences-to-oligotype.fa
o-pad-with-gaps sequences-to-oligotype.fa -o sequences-to-oligotype-padded.fa

# Run MED (where M is the minimum substantive abundance of an oligotype)
# This could take a while depending on the number of reads
decompose sequences-to-oligotype-padded.fa -M 20 

# Reformatting data to use vsearch in order to assign taxonomy
cd sequences-to-oligotype-padded-m0.10-A0-M20-d4
sed 's/-//g' NODE-REPRESENTATIVES.fasta > NODE-REPRESENTATIVES--.fa
mv NODE-REPRESENTATIVES--.fa NODE-REPRESENTATIVES.fa
grep ">" NODE-REPRESENTATIVES.fasta | cut -f 1 -d "|" | sed 's/>//g' > NODE-IDs.txt

# Download SILVA taxonomy table here: https://www.arb-silva.de/
# Store it in a specific directory you will remember, maybe something like "database"
# Mine is: "/Users/Ashley/Documents/database/"
vsearch --usearch_global NODE-REPRESENTATIVES.fa --db /Users/joevineis/scripts/databas/silva119.fa --blast6out NODE-HITS.txt --id 0.6




