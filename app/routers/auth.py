from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=201)
async def register(data: UserRegister):
    existing = await User.find_one(User.email == data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=get_password_hash(data.password),
    )
    await user.insert()
    return {"message": "Usuário criado com sucesso", "id": str(user.id)}


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    user = await User.find_one(User.email == data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
