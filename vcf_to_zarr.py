import sys

import allel
import numpy as np

number_of_samples = 16389
uncalled_threshold = 2 * number_of_samples / 2


class Transformer(object):
    def transform_fields(self, fields):
        return fields

    # add calls while reading to save memory: 0=homo ref, 1=hetero, 2=homo alt, -2=no reads
    # filter out the variants for which the sum over all samples is negative (can't be scaled in pca)
    def transform_chunk(self, chunk):
        calls = chunk['calldata/GT']
        count_uncalled = np.sum(np.sum(calls < 0, axis=2), axis=1)
        call_indexes_to_keep = count_uncalled > uncalled_threshold
        calls_kept = calls[call_indexes_to_keep]
        calls_kept[calls_kept < 0] = 0
        print(f'Kept {len(calls_kept)}')
        chunk['calldata/GT'] = calls_kept


allel.vcf_to_zarr(
    input='./data/aadr_v54.1.p1_1240K_public_eigenstrat_all.vcf_eigenstrat',
    output='./data/aadr_v54.1.p1_1240K_public_eigenstrat_all.zarr',
    fields='*',
    types={'calldata/GT': 'int8'},
    transformers=Transformer(),
    chunk_length=1000,
    chunk_width=-1,
    log=sys.stdout,
    overwrite=True,
)
