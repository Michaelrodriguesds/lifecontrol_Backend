from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.core.config import settings
from app.models.user import User
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

DEV_USER_ID = "dev-user-000000000000"


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> dict:
    if settings.DEV_MODE:
        return {"id": DEV_USER_ID, "name": "Dev User", "email": "dev@lifecontrol.app"}

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )

    user = await User.get(payload.get("sub"))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuário inativo")

    return {"id": str(user.id), "name": user.name, "email": user.email}
