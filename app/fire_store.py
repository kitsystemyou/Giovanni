from google.cloud import firestore, firestore_v1
from model import UpdateText

project_id = "test-gke-360717"


def get_documents(user_id: str, group_id: str):
    db = firestore.Client(project=project_id)
    collections: list[firestore_v1.CollectionReference] = db.collection(user_id).document(group_id).collections(timeout=1)
    docs: dict = {}
    set_list: list = []
    for c in collections:
        doc_snps: list[firestore_v1.DocumentSnapshot] = c.get(timeout=5)
        for doc_snp in doc_snps:
            doc = doc_snp.to_dict()
            doc.update({"id": c.id})
            set_list.append(doc)
    set_list.sort(key=lambda x: x["created_at"], reverse=True)
    docs.update({"result": set_list})
    return docs


def update_documents(user_id: str, group_id: str, update_text: UpdateText) -> dict:
    db = firestore.Client(project=project_id)
    group_collection: firestore_v1.CollectionReference = db.collection(user_id).document(group_id)
    iamge_collection = group_collection.collection(update_text.set_id).document(update_text.name)
    iamge_collection.update({"text": update_text.text})
    print("updated")
    return {"result":
            {"userID": user_id,
             "group_id": group_id,
             "updated_text": update_text
             }
            }
