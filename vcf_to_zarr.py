import sys
import allel
import numpy as np

"""
This script converts a VCF file to a Zarr array, transforming genotype calls in the process.
It uses the scikit-allel library to perform the conversion and custom transformations.

Usage:
- Configure the input VCF file path and output Zarr file path.
- The script transforms genotype calls: 0 for homozygous reference, 1 for heterozygous, 2 for homozygous alternate, -2 for no reads.
- Run the script to perform the conversion and save the output as a Zarr array.

Parameters:
- number_of_samples: Total number of samples in the VCF file.
- uncalled_threshold: Threshold for uncalled genotypes.
- Transformer: Class to transform fields and chunks during the conversion.
- allel.vcf_to_zarr: Function to convert VCF to Zarr with specified settings.
"""

number_of_samples = 16389
uncalled_threshold = number_of_samples * .75


class Transformer(object):
    def transform_fields(self, fields):
        return fields

    def transform_chunk(self, chunk):
        calls = chunk['calldata/GT']
        # Sum up calls: 0=homo ref, 1=hetero, 2=homo alt, -2=no reads
        calls = np.sum(calls, axis=2)
        chunk['calldata/GT'] = calls


allel.vcf_to_zarr(
    input='../data/aadr_v54.1.p1_1240K_public_all.vcf',
    output='../data/aadr_v54.1.p1_1240K_public_all.zarr',
    fields='*',
    types={'calldata/GT': 'int8'},
    transformers=Transformer(),
    chunk_length=1000,
    chunk_width=-1,
    log=sys.stdout,
    overwrite=True,
)
