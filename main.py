from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def authenticate_implicit_with_adc(file: UploadFile):
    # Instantiates a client
    storage_client = storage.Client()

    # The name for the new bucket
    bucket_name = "giovanni-storage"

    destination_blob_name = f'user_id/group_id/{file.filename}'
    print("destination", destination_blob_name)
    # Creates the new bucket
    # bucket = storage_client.create_bucket(bucket_name)
    bucket = storage_client.get_bucket(bucket_name)
    print(f"Bucket {bucket.name} get.")
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file.file)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/files")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/upload")
async def create_upload_file(file: UploadFile):
    print("filename:", file.filename)
    authenticate_implicit_with_adc(file)
    print("end")
    return {"filename": file.filename}


# Snippet
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
