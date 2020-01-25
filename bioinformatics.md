# Bioinformatics Workflow
#### Analysis conducted in QIIME2 (v2019.10) 

Updated by A. Bulseco on 1/23/2020

## Requirements for this workflow
* QIIME2 v2019.10
* R and Phyloseq package 
*Note that some commands may differ for different QIIME2 versions*

## Activate QIIME2 
Activate your working environment (replace "2019.10" with your own version if different)
```source activate qiime2-2019.10 
```
## Demultiplexing
Import sequences as an artifact into QIIME2 
```
qiime tools import \
   --type EMPPairedEndSequences \
   --input-path emp-paired-end-sequences \
   --output-path emp-paired-end-sequences.qza
  ```
 Demultiplex using mapping files 
 *Note: These samples were sequenced in separate sequencing runs; see "combining runs"*
 ```
 qiime demux emp-paired \
  --m-barcodes-file FTR2_mapping_file \
  --m-barcodes-column barcode-sequence \
  --p-rev-comp-mapping-barcodes \
  --i-seqs emp-paired-end-sequences.qza \
  --o-per-sample-sequences demux.qza \
  --o-error-correction-details demux-details.qza

qiime demux summarize \
  --i-data demux.qza \
  --o-visualization demux.qzv
  ```
  
## Running DADA2 
View the output of demultiplexing (demux.qzv) using QIIME2 view to determine where to trim and truncate sequences for forward and reverse reads. In this case, we used the consensus method of Chimera removal and used --p-n-threads 0 to use all available cores. See here for more information on the DADA2 plugin and here for the paper associated with DADA2

```
qiime dada2 denoise-paired \
--i-demultiplexed-seqs demux.qza \
--p-trim-left-f 13 \
--p-trim-left-r 13 \
--p-trunc-len-f 250 \
--p-trunc-len-r 200 \
--o-table table-new-truncated.qza \
--o-representative-sequences rep-seqs-new-truncated.qza \
--o-denoising-stats denoising-stats-new-truncated.qza \
--p-chimera-method consensus \
--p-n-threads 0
```
  
  
