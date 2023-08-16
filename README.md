# Giovanni
Giovanni is an application that manages images and text (extracted from OCR) It is organized as a collection of individual Sets.
Each user can upload their images and centrally manage both the images and the extracted text.
They also have the option to manually edit the text, regardless of whether it was extracted through OCR or not.
Furthermore, it is possible to group and handle each Set collectively.
This feature proves useful when dealing with a large volume of OCR images or when managing images along with descriptive text.

# Backend Overview
- App
  - need: `pipenv` or `python 3.11`
  - use: FastAPI, firestore, firestore_v1

- Cloud Function
  - need: `golang 1.20`, cloud function(or mock of it)
  use

# Feature
main.py: routing(reciept request)
fire_store.py: Call GCP FireStore API
cloud_storage.py: Call GCP CloudStorage API

# Future
We try to do these feature
- improve managing feature
  - manage images as a group
  - make text editable
  - view large image to see whether the OCR result is correct or not.
- improve OCR target (audio)


# File Structure
```
.
├── Dockerfile
├── README.md
├── app // web api
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── cloud_storage.py
│   ├── fire_store.py
│   ├── main.py
│   └── requirements.txt
├── cloud_function // cloud function
│   ├── go.mod
│   ├── go.sum
│   └── main.go
├── cloudbuild.yaml // setting for Cloud Build
└── doc
    └── analyze_sequence.md // TODO
```
