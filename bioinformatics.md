# Bioinformatics Workflow
#### Analysis conducted in QIIME2 (v2019.10) 

Updated by A. Bulseco on 1/23/2020

## Requirements for this workflow
* QIIME2 v2019.10
* R and Phyloseq package 
*Note that some commands may differ for different QIIME2 versions*

## Activate QIIME2 
Activate your working environment (replace "2019.10" with your own version if different)
```
source activate qiime2-2019.10 
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
View the output of demultiplexing (demux.qzv) using QIIME2 view to determine where to trim and truncate sequences for forward and reverse reads. In this case, we used the consensus method of Chimera removal and used --p-n-threads 0 to use all available cores. See here for more information on the DADA2 plugin and [here](https://www.ncbi.nlm.nih.gov/pubmed/27214047) for the paper associated with DADA2

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
## Training the reference database
For our taxonomic analysis, we used the [SILVA 132 release](https://www.arb-silva.de/download/archive/qiime). Download the taxonomy.txt and .fna file and import into QIIME 2 artifacts.
```
qiime tools import \
  --type 'FeatureData[Sequence]' \
  --input-path silva_132_99_16S.fna \
  --output-path 99_perc.qza
  
  qiime tools import \
  --type 'FeatureData[Taxonomy]' \
  --input-format HeaderlessTSVTaxonomyFormat \
  --input-path consensus_taxonomy_7_levels.txt \
  --output-path ref-taxonomy.qza
  ```
#### Extract reference reads
When a Naive Bayes classifier is trained on only the region of the target sequences that was sequenced, in this case the 16S rRNA gene using the 515F/806R pair, it improves taxonomic accuracy. 
```
 qiime feature-classifier extract-reads \
 --i-sequences 99_perc.qza \
 --p-f-primer GTGCCAGCMGCCGCGGTAA \
 --p-r-primer GGACTACHVGGGTWTCTAAT \
 --p-min-length 100 \
 --p-max-length 400 \
 --o-reads ref-seqs-extract.qza
```
#### Train the classifier
There was a mismatch with the version of scikit-learn installed (see error below) and ran an override as suggested by QIIME 2 message boards.

Plugin error from feature-classifier:

The scikit-learn version (0.19.1) used to generate this artifact does not match the current version of scikit-learn installed (0.21.2). Please retrain your classifier for your current deployment to prevent data-corruption errors.
```
conda install --override-channels -c defaults scikit-learn=0.21.2
```
Make sure you have enough disc space for the next few steps  
```
qiime feature-classifier fit-classifier-naive-bayes \
 --i-reference-reads ref-seqs-extract.qza \
 --i-reference-taxonomy ref-taxonomy.qza \
 --o-classifier classifier.qza
```
Apply sequences to the classifer to assign taxonomy
```
qiime taxa collapse \
 --i-taxonomy taxonomy.qza \
 --i-table table-merged-new.qza \
 --p-level 6 \
 --o-collapsed-table table-new-L6.qza

qiime taxa barplot \
 --i-table table-merged-new.qza \
 --i-taxonomy taxonomy.qza \
 --m-metadata-file FTR2_map_all_redo.txt \
 --o-visualization taxa-bar-plots-all.qzv
```

# Filtering data
In the next step, we will filter out the following: 
* By taxonomic groups: Archaea, chloroplasts, mitochondria
* By samples: those with < 1000 sequences per sample
* By features: singletons < 2 

```
mkdir filtered-data
qiime feature-table filter-samples \
--i-table table-merged-new.qza \
--p-min-frequency 1000 \
--o-filtered-table filtered-data/table-nolow.qza

# Then summarize to confirm the data were filtered out
qiime feature-table summarize \
--i-table filtered-data/table-nolow.qza \
--o-visualization filtered-data/table-nolow.qzv


  
