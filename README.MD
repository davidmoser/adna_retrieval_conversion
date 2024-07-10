# Allen DNA Database Scripts

## Overview
This project provides scripts for downloading and converting ancient DNA data from the Allen Ancient DNA Database.

[Allen Ancient DNA Resource](https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data)

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
