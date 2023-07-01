from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from cloud_storage import authenticate_implicit_with_adc
from fire_store import get_documents


app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://giovanniweb-onjvsvnita-uc.a.run.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload/{user_id}/{group_id}")
async def create_upload_file(file: UploadFile, user_id: str, group_id: str):
    print("filename:", file.filename)
    authenticate_implicit_with_adc(file, user_id, group_id)
    return {"filename": file.filename}


@app.get("/collection/{user_id}/{group_id}")
async def get_items(user_id, group_id: str):
    dict_docs = get_documents(user_id, group_id)
    return dict_docs

