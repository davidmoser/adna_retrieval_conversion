# Allen DNA Database Scripts

## Overview

This project provides scripts for downloading and converting ancient DNA data from
the [Allen Ancient DNA Resource](https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data).

## Formats

### Packed ancestrymap
`.ancestrymap`: Storage optimized format by David Reich group, format of downloaded files. [Link](https://reich.hms.harvard.edu/software/InputFileFormats)

### Eigenstrat format
`.snp`, `.geno`: Format used by EIGENSTRAT software. [Link](https://reich.hms.harvard.edu/software/InputFileFormats)

### Variance call format
`.vcf`: Standard text format for variation data. [Link](https://www.ebi.ac.uk/training/online/courses/human-genetic-variation-introduction/variant-identification-and-analysis/understanding-vcf-format/)

## Convertf

The initial conversion is from packed ancestrymap to eigenstrat with the EIG C-based software.
Pull, compile and run convertf in [Github for EIG](https://github.com/DReichLab/EIG). There are some details in `comments.txt`.

## Scripts

### `download_database.py`

Downloads Eigenstrat data from the Allen Ancient DNA Database.

### `vcf2eigenstrat.py`

Converts VCF files to Eigenstrat format.

### `eigenstrat2vcf.py`

Converts Eigenstrat files to VCF format.

### `vcf_to_zarr.py`

Saves VCF data as a Zarr array.

### `rearrange_zarr.py`

Rearranges the chunking dimension of a Zarr array for machine learning.
