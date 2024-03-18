# Importing necessary libraries from Azure Storage SDK
from azure.storage.blob import BlobServiceClient

class BlobUtil:
    def __init__(self):
        print("init")

    # Function to upload a file to Azure Blob Storage container
    def upload_blob(self, file):
        print("Invoked upload_blob")
        """
        Uploads a file to Azure Blob Storage container.
        """

        # Your Azure Storage Account connection string
        connection_string = "DefaultEndpointsProtocol=https;AccountName=ctrlaltdefeatstorage;AccountKey=6QcBlepAUMysjJu15Y9v8sfICUUovvZYaUNj8x6JiidFnYPzy6C8LnAcnDU5Ifyk3GqTaDeQRrHn+AStxWhtVA==;EndpointSuffix=core.windows.net"
        
        # Name of the container in Azure Blob Storage
        container_name = "ctrlaltdefeatpdfcontainer"

        # Creating a BlobServiceClient object using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Creating a ContainerClient object for the specified container
        container_client = blob_service_client.get_container_client(container_name)

        # Name of the destination blob (same as the uploaded file name)
        destination_blob_name = file.name

        # Printing the file to be uploaded and its destination
        print(f'Uploading file: {file.name} to destination: {destination_blob_name}')

        # Uploading the file to the container
        blob_client = container_client.get_blob_client(destination_blob_name)
        #with open(file.name, "rb") as data:
        blob_client.upload_blob(file)

        # Printing a confirmation message after successful upload
        print(f'File: {file.name} uploaded to destination: {destination_blob_name}')


    # Function to generate URL for accessing a blob in Azure Blob Storage container
    def get_blob_url(self, blob_name):
        """
        Generates a URL to access a blob in Azure Blob Storage container.
        """

        # Your Azure Storage Account connection string
        connection_string = "DefaultEndpointsProtocol=https;AccountName=ctrlaltdefeatstorage;AccountKey=6QcBlepAUMysjJu15Y9v8sfICUUovvZYaUNj8x6JiidFnYPzy6C8LnAcnDU5Ifyk3GqTaDeQRrHn+AStxWhtVA==;EndpointSuffix=core.windows.net"
        
        # Name of the container in Azure Blob Storage
        container_name = "ctrlaltdefeatpdfcontainer"

        # Creating a BlobServiceClient object using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Generating the URL for the specified blob
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"
        return blob_url
