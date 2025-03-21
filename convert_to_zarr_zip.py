# Convert directory zarr to zipped zarr, there's no direct ZipStore support in scikit-allel
import zarr
from shutil import rmtree
from zipfile import ZIP_STORED

def convert_to_zarr_zip(directory_zarr_path, remove_directory=False):
    dir_store = zarr.DirectoryStore(directory_zarr_path)
    # No additional compression, see compression setting in vcf2zarr.zip
    zip_store = zarr.ZipStore(directory_zarr_path + ".zip", mode="w", compression=ZIP_STORED)
    zarr.copy_store(dir_store, zip_store)
    zip_store.close()
    if remove_directory:
        rmtree(directory_zarr_path)