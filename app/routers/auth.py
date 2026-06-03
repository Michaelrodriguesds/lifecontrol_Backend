from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserInfo
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: UserRegister):
    """
    Cadastra um novo usuário e já retorna os tokens + dados do usuário.

    ⚠️ PROBLEMA CORRIGIDO:
    Antes o register retornava apenas {"message": ..., "id": ...}.
    O auth.service.ts tentava salvar res.access_token que era undefined,
    deixando o localStorage vazio. Resultado: todas as requisições
    seguintes iam sem o header Authorization → 401 em tudo.
    Agora o register retorna o mesmo formato que o login.
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

    access_token  = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserInfo(id=str(user.id), name=user.name, email=user.email),
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    """
    Autentica e retorna tokens JWT + dados do usuário.
    """
    user = await User.find_one(User.email == data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token  = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserInfo(id=str(user.id), name=user.name, email=user.email),
    )


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    """
    Valida o token e retorna os dados do usuário logado.
    Chamado pelo checkToken() ao recarregar a página.
    """
    return current_user