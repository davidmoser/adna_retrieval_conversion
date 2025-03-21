import random
import time

import zarr


def benchmark_zarr(array, consecutive, axis, nb_batches, batch_size):
    if axis > 1:
        raise ValueError("axis must be 0 or 1")
    # Open the zarr store in read mode
    total_rows = array.shape[axis]
    total_time = 0.0

    if consecutive:
        # For consecutive access, assume starting at row 0 and stepping by batch size.
        for i in range(nb_batches):
            start_index = i * batch_size
            # If there are not enough rows for another batch, break.
            if start_index + batch_size > total_rows:
                break
            start_time = time.time()
            if axis == 0:
                batch = array[start_index:start_index + batch_size]
            else:
                batch = array[:, start_index:start_index + batch_size]
            end_time = time.time()
            total_time += (end_time - start_time)
    else:
        # For random access, randomly choose a valid starting index for each batch.
        for i in range(nb_batches):
            start_index = random.randint(0, total_rows - batch_size)
            start_time = time.time()
            if axis == 0:
                batch = array[start_index:start_index + batch_size]
            else:
                batch = array[:, start_index:start_index + batch_size]
            end_time = time.time()
            total_time += (end_time - start_time)

    return total_time


store_paths = [
    "zarr/v62.0_1240k_public.zarr",
    "zarr/v62.0_1240k_public_arranged.zarr"
]

nb_batches = 10
batch_size = 128
axis = 0
internal_path = "calldata/GT"

print("Benchmarking: {nb_batches} batches of {batch_size} rows")
for store_path in store_paths:
    array = zarr.open(store_path, mode="r")[internal_path]

    print(f"Store: {store_path} | Shape: {array.shape}")
    for flag, access_type in [(True, "consecutive"), (False, "random")]:
        elapsed = benchmark_zarr(array, flag, axis, nb_batches, batch_size)
        print(f"{access_type}: {elapsed:.6f} s")
