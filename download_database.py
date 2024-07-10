from pyDataverse.api import NativeApi, DataAccessApi

"""
This script downloads all files from a specified dataset in the Allen Ancient DNA Database hosted on Dataverse.
The script uses the pyDataverse library to interact with the Dataverse API, retrieve the dataset, and download each file.

Usage:
- Set the base_url to the Dataverse instance URL.
- Replace DOI with the dataset DOI.
- Run the script to download all files from the dataset.
"""

# Set the base URL of the Dataverse
base_url = 'https://dataverse.harvard.edu/'

# Create API instances
api = NativeApi(base_url)
data_api = DataAccessApi(base_url)

# DOI of the Allen Ancient DNA Database
DOI = "https://doi.org/10.7910/DVN/FFIDCW"

# Get the dataset
dataset = api.get_dataset(DOI)

# Check if the dataset retrieval was successful
if dataset.status_code != 200:
    raise Exception("Dataset not found. Check the DOI.")

# Get the list of datafiles in the dataset
files_list = dataset.json()['data']['latestVersion']['files']

# Download each file
for file in files_list:
    filename = file["dataFile"]["filename"]
    file_id = file["dataFile"]["id"]
    file_size = file["dataFile"]["filesize"]
    print(f"Downloading file: {filename}, id: {file_id}, size: {file_size}")

    response = data_api.get_datafile(file_id)
    if response.status_code != 200:
        print(f"Failed to download file: {filename}")
        continue

    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"File downloaded: {filename}")

print("All files downloaded.")
