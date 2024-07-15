#from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import json
import argparse

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

connection_string = config.get('connection_string')
connection_url = config.get('connection_url')
use_key = config.get('use_key', False)

container_name = config.get('container_name')
blob_name = config.get('blob_name')
file_path = config.get('file_path')

def upload_blob():
    # Create a BlobServiceClient object
    if use_key:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    else:
        blob_service_client = BlobServiceClient(account_url=connection_url)

    # Create the container if it does not exist
    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.create_container()
    except Exception as e:
        print(f"Container already exists: {e}")

    # Create a BlobClient object
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Upload the file
    with open(file_path, 'rb') as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {file_path} to {blob_name} in {container_name} container.")

if __name__ == '__main__':
    upload_blob()