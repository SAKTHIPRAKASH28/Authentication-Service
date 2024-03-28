from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
import asyncio
import motor.motor_asyncio
load_dotenv()
username = quote_plus(os.getenv("MONGO_USERNAME"))
password = quote_plus(os.getenv("MONGO_PASSWORD"))
uri = 'mongodb+srv://' + username + ':' + password + \
    '@cluster0.shvj8sa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client["lost_and_found"]["users"]


async def get_user_creds(username):
    user = await db.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"])
    return user


async def set_user_creds(username, password):
    try:
        await db.insert_one({"username": username, "password": password})
    except Exception as e:
        raise e


async def main():
    await set_user_creds("Sakthiprakash40", "example")
    res = await get_user_creds("Sakthiprakash40")
    print(res['_id'])

if __name__ == '__main__':
    asyncio.run(main())
