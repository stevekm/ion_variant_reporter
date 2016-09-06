#!/usr/bin/env python
# python 2.7

# need to get the UCSC Known Canonical Transcripts
# UCSC transcripts with unique ID's (also available for hg38)
# http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/knownCanonical.txt.gz
# need to match 5th col ID's with RefGene ID's from here:
# http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/kgXref.txt.gz
# # https://groups.google.com/a/soe.ucsc.edu/forum/#!topic/genome/_6asF5KciPc


import sys
import os
import pandas as pd

crossref_file = "/ifs/home/kellys04/projects/clinical_genomic_reporting/clinical_genomics_development/data/hg19/kgXref.txt"
canon_file = "/ifs/home/kellys04/projects/clinical_genomic_reporting/clinical_genomics_development/data/hg19/knownCanonical.txt"
outdir= "/ifs/home/kellys04/projects/clinical_genomic_reporting/clinical_genomics_development/data/hg19"

# df of the crossrefence ID's
cross_cols = ['UCSC_id', 'B', 'C', 'D', 'Gene', 'Ref_id', 'G', 'Description', 'I']
crossref_df = pd.read_table(crossref_file,sep='\t', header = None, index_col=False, names = cross_cols) # 


# get list of UCSC ID's for canonical transcripts
canon_cols = ['Chrom', 'Start', 'Stop', 'Num', 'UCSC_id']
canon_df = pd.read_table(canon_file,sep='\t', header = None, index_col=False, names = canon_cols)

# merge the df's 
merge_df = pd.merge(canon_df, crossref_df, on = 'UCSC_id', how = 'inner')

# remove some cols
cols_to_keep = ['UCSC_id', 'Ref_id', 'Chrom', 'Start', 'Stop', 'Gene', 'Description']
merge_df = merge_df[merge_df.columns.drop([col for col in merge_df.columns if col not in cols_to_keep])]

# save file
merge_df.to_csv(outdir + "/" + "canonical_transcript_table.tsv", sep='\t', index=False)

# peel off just the transcripts
canon_refs = merge_df['Ref_id'].dropna()
canon_refs.drop_duplicates(inplace = True)
canon_refs.to_csv(outdir + "/" + "canonical_transcript_list.tsv", sep='\t', index=False)
