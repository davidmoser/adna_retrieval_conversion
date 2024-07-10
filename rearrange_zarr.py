import zarr

"""
In the original files vcf/eigenstrat, one row is one SNP
for learning it's optimal to rearrange so that one row is one sample
in the resulting zarr array:
- Dim 0 is the sample dimension
- Dim 1 is the SNP dimension
- Dim 0 is chunked with "chunk_size"
- Dim 1 is not chunked
That means array[i] will retrieve all the SNPs for sample i which reside in a single file
It also means that retrieving all sample values for one SNP is array[:,j] and will retrieve
all the files. So, filtering or normalization of SNPs should happen before rearranging
"""

original_store = '../data/aadr_v54.1.p1_1240K_public_all.zarr'
zarr_path = 'calldata/GT'
rearranged_store = '../data/aadr_v54.1.p1_1240K_public_all_arranged.zarr'
# samples per chunk in rearranged file
chunk_size = 1

# Open the original zarr array
original_array = zarr.open(original_store, mode='r')[zarr_path]

# Get the shape of the original array
shape = original_array.shape

chunk_shape = original_array.chunks
if chunk_shape[1] != shape[1]:
    raise ValueError('Iteration below only works if no chunking along dim 1')

# Create a new zarr array with switched dimensions
new_array = zarr.zeros((shape[1], shape[0]), chunks=(chunk_size, shape[0]), store=rearranged_store, path=zarr_path,
                       overwrite=True, dtype='int8')

# Iterate over the chunks along the first dimension (chunks of multiple SNPs) and copy them to the new array
write_chunk_size = 20 * chunk_shape[0]
for i in range(0, shape[0], write_chunk_size):
    print(f"Writing chunk starting at {i}")
    chunk_start = i
    chunk_end = min(i + write_chunk_size, shape[0])
    chunk = original_array[chunk_start:chunk_end, :]
    new_array[:, chunk_start:chunk_end] = chunk.T
