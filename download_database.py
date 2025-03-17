import os
import requests

"""
This script downloads all files from a specified dataset in the Allen Ancient DNA Database hosted on Dataverse.
The script uses the pyDataverse library to interact with the Dataverse API, retrieve the dataset, and download each file.
"""


def download_file(url, dest_path):
    """Download a file from the specified URL and save it to dest_path."""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive chunks
                    f.write(chunk)


def main():
    # Customize these variables
    dataverse_base = "https://dataverse.harvard.edu"  # Change to your Dataverse host
    dataset_persistent_id = "doi:10.7910/DVN/FFIDCW"  # Change to your dataset's persistent ID
    output_folder = "data"

    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get dataset metadata using the persistentId
    metadata_url = f"{dataverse_base}/api/datasets/:persistentId/?persistentId={dataset_persistent_id}"
    response = requests.get(metadata_url)
    response.raise_for_status()
    dataset_metadata = response.json()

    # Extract list of files from the dataset metadata
    files_list = dataset_metadata['data']['latestVersion']['files']

    print(f"Found {len(files_list)} file(s) to download.")

    # Download each file
    for file_info in files_list:
        file_id = file_info['dataFile']['id']
        file_label = file_info.get('label', f"file_{file_id}")
        print(f"Downloading: {file_label} (ID: {file_id})")

        # Build the download URL using the file id
        download_url = f"{dataverse_base}/api/access/datafile/{file_id}"
        dest_path = os.path.join(output_folder, file_label)

        try:
            download_file(download_url, dest_path)
            print(f"Downloaded: {dest_path}")
        except Exception as e:
            print(f"Error downloading {file_label}: {e}")


if __name__ == '__main__':
    main()
