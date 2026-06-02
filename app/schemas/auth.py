from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ⚠️ PROBLEMA CORRIGIDO:
# O TokenResponse original não incluía dados do usuário.
# O auth.service.ts do Angular tentava ler res.user e ficava undefined,
# então currentUser nunca era preenchido corretamente.
# Adicionamos o objeto UserInfo embutido na resposta do login.
class UserInfo(BaseModel):
    id: str
    name: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Optional[UserInfo] = None   # ← novo campo para o frontend
