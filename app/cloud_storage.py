from fastapi import UploadFile
from google.cloud import storage


def authenticate_implicit_with_adc(file: UploadFile, user_id: str, group_id: str):
    # Instantiates a client
    storage_client = storage.Client()

    # The name for the root bucket
    bucket_name = "giovanni-storage"

    destination_blob_name = f'{user_id}/{group_id}/{file.filename}'
    print("destination", destination_blob_name)
    bucket = storage_client.get_bucket(bucket_name, timeout=5)
    print(f"Bucket {bucket.name} get.")
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file.file, timeout=10)
