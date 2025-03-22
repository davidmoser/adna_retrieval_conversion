# Allen Ancient DNA Resource Scripts

## Overview

This project provides scripts to download ancient DNA data from
the [Allen Ancient DNA Resource](https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data)
and to convert it to other formats.

## Formats

### Packed ancestrymap

`.ancestrymap`: Format of the downloaded files. Storage optimized format by David Reich
group. [Link](https://reich.hms.harvard.edu/software/InputFileFormats)

### Eigenstrat format

`.snp`, `.geno`: Format used by EIGENSTRAT software. [Link](https://reich.hms.harvard.edu/software/InputFileFormats)

### Variance call format

`.vcf`: Standard text format for variation
data. [Link](https://www.ebi.ac.uk/training/online/courses/human-genetic-variation-introduction/variant-identification-and-analysis/understanding-vcf-format/)

### Zarr format

Format to store multidimensional arrays in chunks for efficient access.
Enables fast access to rows (SNPs) and columns (samples) without loading the entire table.

## Download and Conversion

### Download Ancestrymap Data

Run the `download_ancestrymap.py` script.
It downloads the ancestrymap data from the Allen Ancient DNA Database and places it in the `ancestrymap` folder.

### Convert Ancestrymap to Eigenstrat

First compile or download the `convertf` binary.
Adjust the filenames in the `config/ancestrymap2eigenstrat.params` file to match the current filenames.
You may also have to adjust the location of the `convertf` binary.
Then run the `ancestrymap2eigenstrat.sh` script.

### Convert Eigenstrat to VCF

Adjust the filenames in the `config/eigenstrat2vcf.yaml` file to match the current filenames.
Make sure the have the dependencies installed with the versions given in `requirements.txt`, scikit doesn't work
with zarr version 3 or higher.
Run the `eigenstrat2vcf.py` script.

### Convert VCF to Zarr SNP chunked

Adjust the filenames in the `config/vcf2zarr.yaml` file to match the current filenames.
The chunking parameters can be set. Using -1 will not chunk that direction. The SNP direction should be chunked since
that's the number of lines the script reads in the VCF file before writing a chunk.
Then run the `vcf2zarr.py` script.

## Convert to Zarr individual/sample chunked

This converts the Zarr file that is SNP chunked to one that's individual chunked for efficient iteration and random
access to all SNP calls of a single individual.
Adjust the filenames and the chunking size in `config/rearrange_zarr.yaml`, then run the `rearrange_zarr.py` script.

## Convertf

The first conversion from packed ancestrymap to eigenstrat is done with be C-program Convertf.
Pull [Github for EIG](https://github.com/DReichLab/EIG) next to the `adna_retrieval_conversion` repo (else you'll have
to adjust the convertf location in the bash script).

Install dependencies

```
sudo apt install libopenblas-dev
sudo apt install libgsl-dev
sudo apt install liblapacke-dev
```

Change to `src` folder and in the `Makefile` file uncomment line 5: `override LDLIBS += -llapacke`.

Then compile with

```
make
make install
```