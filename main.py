from fastapi import (FastAPI, status, Depends)
from fastapi.responses import JSONResponse
from src.utils import *
from src.emailotp import *

app = FastAPI()


@app.post("/addUser", status_code=status.HTTP_201_CREATED)
async def new_user(user: NewUser,otp:str=None):
    if not otp:
        try:
            return JSONResponse(content=send_email(user.email),status_code=201)
        except HTTPException as e:
            return JSONResponse(content={"error": str(e)}, status_code=e.status_code)
    else:
        try :
            validate_otp(user.email,otp)
            result = await add_user(user.username, user.password,user.email)
            return JSONResponse(content=result,status_code=201)
        except HTTPException as e:
            return JSONResponse(content={"error": str(e)}, status_code=e.status_code)


@app.post("/getJwt", status_code=status.HTTP_201_CREATED)
async def generate_JWT(user: UserModel):
    try:
        result, _id = await verify_password(user.username, user.password)
        if result:
            token = await generate_tokens(600, _id)
            return JSONResponse(content=token,status_code=201)
        else:
            return JSONResponse(status_code=401, content="Invalid credentials")
    except HTTPException as e:
            return JSONResponse(content={"error": str(e)}, status_code=e.status_code)

@app.post("/refresh", status_code=status.HTTP_201_CREATED)
async def refresh(token: str):
    try:
        await refresh_token(token)
    except HTTPException as e:
            return JSONResponse(content={"error": str(e)}, status_code=e.status_code)


if __name__ == '__main__':
    import os
    import uvicorn
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, reload=True)
