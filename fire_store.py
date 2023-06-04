from google.cloud import firestore, firestore_v1

project_id = "test-gke-360717"


def get_documents(user_id: str, group_id: str):
    db = firestore.Client(project=project_id)
    collections: list[firestore_v1.CollectionReference] = db.collection(user_id).document(group_id).collections(timeout=5)
    print("got collections")
    docs: dict = {}
    for c in collections:
        for doc in c.stream(timeout=5):
            print(f'{doc.id}')
            docs.update({c.id: {doc.id: doc.to_dict()}})
    print(len(docs))
    print(f'user_id: {user_id}, group_id: {group_id}')
    return docs
