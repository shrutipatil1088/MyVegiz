from app.db.session import SessionLocal
# Gives DB session to routes

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



from fastapi import Depends, Header
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.security import SECRET_KEY, ALGORITHM
from app.core.exceptions import AppException
from app.models.user import User
from app.api.dependencies import get_db
from app.models.token_blacklist import TokenBlacklist


def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    # Expect: Authorization: Bearer <token>
    if not authorization.startswith("Bearer "):
        raise AppException(status=401, message="Invalid authorization header")

    token = authorization.split(" ")[1]

    # ❌ BLOCK LOGGED-OUT TOKENS
    blacklisted = db.query(TokenBlacklist).filter(
            TokenBlacklist.token == token
        ).first()
    if blacklisted:
        raise AppException(status=401, message="Token expired. Please login again")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

    except JWTError:
        raise AppException(status=401, message="Token expired or invalid")

    user = db.query(User).filter(
        User.id == user_id,
        User.is_active == True,
        User.is_delete == False
    ).first()

    if not user:
        raise AppException(status=401, message="User not authorized")

    return user
