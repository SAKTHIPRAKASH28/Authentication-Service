from fastapi import (FastAPI, status, Depends)
from utils import *


app = FastAPI()


@app.post("/addUser", status_code=status.HTTP_201_CREATED)
async def new_user(user: UserModel):
    result = await add_user(user.username, user.password)
    return result


@app.post("/getJwt", status_code=status.HTTP_201_CREATED)
async def generate_JWT(user: UserModel):
    result, _id = await verify_password(user.username, user.password)
    if result:
        token = await generate_tokens(600, _id)
        return token
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/refresh", status_code=status.HTTP_201_CREATED)
async def refresh(token: str):
    return await refresh_token(token)


if __name__ == '__main__':
    import os
    import uvicorn
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, reload=True)
