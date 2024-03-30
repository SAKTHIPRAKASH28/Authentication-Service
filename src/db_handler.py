import os
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate(
    "./lost-and-found-2c2e1-firebase-adminsdk-g74lw-e6257f3cf5.json")

firebase_admin.initialize_app(cred)

db = firestore.client()
collection_ref = db.collection("Users")


def get_user_creds(username):
    query = collection_ref.where("username", "==", username).limit(1)
    users = query.stream()

    for user in users:
        user_data = user.to_dict()
        user_data["_id"] = user.id
        return user_data

    return None


def set_user_creds(username, password):
    try:
        collection_ref.add({"username": username, "password": password})
    except Exception as e:
        raise e


async def main():
    set_user_creds("Sakthiprakash40", "example")
    res = get_user_creds("Sakthiprakash40")
    print(res["_id"])

if __name__ == '__main__':
    asyncio.run(main())
