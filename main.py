from azure.storage.blob import *


print("Welcome to the file size calculator for Azure Storage on Python")
print("What is your storage account name?")
SAName = input()
print("what is your key?")
SAKey = input()
print("what kind of file path are you curious about getting the size on? (ex. .vhd, .png, .gif, etc.")
fileType = input()

block_blob_service = BlockBlobService(account_name=SAName, account_key=SAKey)
containers = block_blob_service.list_containers()

marker = None;
sizeOfFileTypes = 0
blobsList = []

print("Printing out containers:")
for c in containers:
    print("     " + c.name + ":")
    blobs = block_blob_service.list_blobs(c.name, marker=marker)
    blobsList.extend(blobs)
    for blob in blobsList:
        blob_property = BlockBlobService.get_blob_properties(block_blob_service, c.name, blob.name)
        print("Blob name: " + blob.name)
        print("Blob size: " + str(blob_property.properties.content_length))
        if str(blob_property.name).endswith(fileType):
            sizeOfFileTypes += blob_property.properties.content_length
print("Total size of " + fileType + " files: " + str(sizeOfFileTypes))