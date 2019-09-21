# Code to demultiplex samples using Illumina utils (https://github.com/merenlab/illumina-utils)
# Code modified from Joe Vineis (https://github.com/jvineis/med-anvio-workshop/wiki/Demultiplexing-and-quality-filtering-Illumina-fastq)
# Need r1 (forward), r2 (reverse), and index (mapping file) i.e. "samples-to-barcode" 

# Ensure the raw fastq files from the MiSeq are gunzipped
gzip forward.fastq

# Create a directory for demultiplexed reads
# Demultiplex 
mkdir demultiplex 
iu-demultiplex -s samples-to-barcode.txt --r1 forward.fastq.gz --r2 reverse.fastq.gz --index barcodes.fastq -o demultiplexed -x

# Create a configs file and merge paired reads
iu-gen-configs 00_DEMULTIPLEXING_REPORT

# "ls" lists all file that end with an .ini, "sed" is a find and replace tool
# ">" creates a new file. We are finding "*\.ini" and replacing it with ""
# use forward slash before because unix hates dots
ls *.ini | sed 's/\.ini//g' > samples.txt  
gunzip *.ini # we have to unzip the fastq files to run the following code
for i in `cat samples.txt`; do iu-merge-pairs $i'.ini' -o $i'-merged' --enforce-Q30-check; done

# You can look at a summary of the merging by looking at "STATS" 
# FAILED are reads that failed to merge
# FAILED_Q30 are reads that failed quality check
# FAILED_WITH_Ns whether you get rid of reads with Ns
# MERGED success! This file will specify the number of mismatches for a single read. If there is a mismatch, it takes the read for which the quality score is highest. 
# MISMATCHES_BREAKDOWN mismatches found in merged region between reads

# Filter out the reads that have more than three mismatches
for i in `cat samples.txt`; do iu-filter-merged-reads $i'-merged_MERGED' -m 3; done


