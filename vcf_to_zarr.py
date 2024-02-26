import sys

import allel
import numpy as np

number_of_samples = 16389
uncalled_threshold = number_of_samples * .75


class Transformer(object):
    def transform_fields(self, fields):
        return fields

    def transform_chunk(self, chunk):
        calls = chunk['calldata/GT']
        # sum up calls: 0=homo ref, 1=hetero, 2=homo alt, -2=no reads
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
