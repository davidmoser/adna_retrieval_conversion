import sys

import allel
import numpy as np
import yaml

import zarr
from convert_to_zarr_zip import convert_to_zarr_zip

"""
This script converts a VCF file to a Zarr array, transforming genotype calls in the process.
It uses the scikit-allel library to perform the conversion and custom transformations.

Remarks:
- Configure the parameters in config/vcf2zarr.yaml
- The script transforms genotype calls: 0 for homozygous reference, 1 for heterozygous, 2 for homozygous alternate, -2 for no reads.
- Run the script to perform the conversion and save the output as a Zarr array.
"""


class Transformer(object):
    def transform_fields(self, fields):
        return fields

    def transform_chunk(self, chunk):
        calls = chunk['calldata/GT']
        # Sum up calls: 0=homo ref, 1=hetero, 2=homo alt, -2=no reads
        calls = np.sum(calls, axis=2)
        chunk['calldata/GT'] = calls


def vcf_to_zarr(vcf_file, zarr_file, ind_chunk, snp_chunk):
    allel.vcf_to_zarr(
        input=vcf_file,
        output=zarr_file,
        compressor=zarr.Blosc(cname='zstd', clevel=5, shuffle=0),
        fields='*',
        types={'calldata/GT': 'int8'},
        transformers=Transformer(),
        chunk_length=snp_chunk,  # SNPs chunked together
        chunk_width=ind_chunk,  # individuals chunked together
        log=sys.stdout,
        overwrite=False,
    )
    if zarr_file.endswith('.zip'):
        convert_to_zarr_zip(zarr_file.removesuffix(".zip"), remove_directory=True)


def vcf_to_zarr_yaml(file_path):
    # Load config and call the main function with appropriate parameters.
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)

    # Extract required and optional parameters
    vcf_file = config.get("vcf_file")
    zarr_file = config.get("zarr_file")
    ind_chunk = config.get("ind_chunk", None)  # Optional
    snp_chunk = config.get("snp_chunk", None)  # Optional

    vcf_to_zarr(vcf_file, zarr_file, ind_chunk, snp_chunk)


if __name__ == "__main__":
    vcf_to_zarr_yaml("config/vcf2zarr.yaml")
