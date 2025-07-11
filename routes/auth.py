import json
import os
import requests
from fastapi import APIRouter, HTTPException, Request, Response, Depends, Cookie
from fastapi.responses import (JSONResponse, Response)
from services.users_services import UserServices
from db.base import Database
from models.Users import Users
from dotenv import load_dotenv

load_dotenv()
DOMAIN = os.getenv("DOMAIN")
CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET")

db = Database()

router = APIRouter(prefix="/auth")


async def get_access_token(code: str):
    """
    Обмен кода авторизации на токен доступа.
    """
    token_url = "https://oauth.yandex.ru/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Ошибка при получении токена")
    print(response.json())
    return response.json().get("access_token")


@router.get("/get_cookie")
async def get_cookie(request: Request):
    try:
        cookies = request.cookies
        return Response(content=json.dumps(cookies), status_code=200)
    except Exception as e:
        return Response(content=json.dumps({"error": str(e)}), status_code=500)


@router.get("/current-user")
async def get_current_user(user_id: str = Cookie(None)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    async with db.session_factory() as session:
        user = await session.get(Users, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"id": user.id, "username": user.username}
    

@router.get("/sign-in")
async def auth_login(
    request: Request,
    response: Response,
    nickname: str,
    hashed_password: str,
    db: Database = Depends(Database),
):
    try:
        obj = {"nickname": nickname, "hashed_password": hashed_password}

        user_model = UserServices(db)

        user = await user_model.logging(obj)

        if user:
            # token = await token_model.new_token(obj=obj, user_id=user.id)
            usr_id = user.id
            response = JSONResponse(
                content=json.dumps(
                    {"status": "Successfully", "user_id": str(usr_id)}
                ),
                status_code=200,
            )
            return response
        return {"status": "error", "message": "Неправильный логин или пароль"}
    except Exception as e:
        print(e)
        return {"message": str(e)}
    

@router.get("/check_token")
async def check_token(code: str, db: Database = Depends(Database)):
    try:
        # 1. Проверяем токен в БД
        user_services = UserServices(db)
        token = await get_access_token(code)
        print("TOKEN:", token)
        existing_user = await user_services.check_yandex_token(token)
        print(existing_user)
        if existing_user:
            print("SEND success")
            response_data = {
                "status": "authenticated",
                "user_id": str(existing_user.id),
                "username": existing_user.username,
                "action": "login",
                "success": True,
            }
            return JSONResponse(
                content=response_data,
                headers={
                    "Access-Control-Allow-Origin": DOMAIN,  
                },
            )

        try:
            profile = await user_services.get_yandex_profile(token)
            login = profile.get("login")
            email = profile.get("default_email", "None")
            birthday = profile.get("birthday", "None")
            # Проверки на пустые поля
            email = email if email else None
            login = login if login else None
            birthday = birthday if birthday else "hui"
            if not login:
                raise HTTPException(
                    status_code=400, detail="Не удалось получить логин Яндекса"
                )

            new_user = await user_services.create_new_user(
                email=email,
                password="12345",
                username=login,
                birthday=birthday,
                yandex_token=token,
                rooms_list=[],
            )

            return JSONResponse(
                {
                    "status": "registered",
                    "user_id": str(new_user["user_id"]),
                    "username": login,
                    "action": "register",
                    "success": True,
                }
            )
        except Exception as e:
            print(str(e))

    except HTTPException:
        raise
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")