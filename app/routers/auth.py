from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserInfo
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=201)
async def register(data: UserRegister):
    """
    Cadastra um novo usuário.
    Verifica se o e-mail já existe antes de criar.
    """
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
    """
    Autentica o usuário e retorna tokens JWT + dados do usuário.

    ⚠️ PROBLEMA CORRIGIDO:
    Antes a resposta só retornava os tokens (access_token, refresh_token).
    O Angular tentava ler res.user e recebia undefined, então o
    currentUser signal nunca era preenchido.
    Agora retornamos também o objeto user com id, name e email.
    """
    user = await User.find_one(User.email == data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token  = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        # Retornamos os dados básicos do usuário para o frontend
        user=UserInfo(id=str(user.id), name=user.name, email=user.email),
    )


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado pelo token JWT.

    ⚠️ PROBLEMA CORRIGIDO — ENDPOINT FALTANTE:
    O auth.service.ts chama GET /api/auth/me no checkToken() para
    validar o token salvo no localStorage e recuperar os dados do
    usuário ao recarregar a página. Esse endpoint não existia,
    causando erro 404 e logout imediato.
    """
    return current_user
