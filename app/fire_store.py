from google.cloud import firestore, firestore_v1

project_id = "test-gke-360717"


def get_documents(user_id: str, group_id: str):
    db = firestore.Client(project=project_id)
    collections: list[firestore_v1.CollectionReference] = db.collection(user_id).document(group_id).collections(timeout=1)
    print("got collections")
    docs: dict = {}
    set_list: list = []
    for c in collections:
        doc_snps: list[firestore_v1.DocumentSnapshot] = c.get(timeout=5)
        for doc_snp in doc_snps:
            print(doc_snp.to_dict())
            doc = doc_snp.to_dict()
            doc.update({"id": c.id})
            set_list.append(doc)
    print(f'user_id: {user_id}, group_id: {group_id}')
    set_list.sort(key=lambda x: x["created_at"], reverse=True)
    docs.update({"result": set_list})
    return docs


# TODO update document