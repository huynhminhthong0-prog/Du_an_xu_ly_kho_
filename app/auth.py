
from datetime import datetime, timedelta, timezone
import os

import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models


# =========================
# CAU HINH JWT
# =========================

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# =========================
# DATABASE
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# HASH MAT KHAU
# =========================

def bam_mat_khau(mat_khau: str) -> str:
    return bcrypt.hashpw(
        mat_khau.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def kiem_tra_mat_khau(
    mat_khau: str,
    mat_khau_bam: str
) -> bool:
    try:
        return bcrypt.checkpw(
            mat_khau.encode("utf-8"),
            mat_khau_bam.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


# =========================
# TAO JWT
# =========================

def tao_access_token(
    data: dict,
    thoi_gian_song: timedelta | None = None
) -> str:
    du_lieu = data.copy()

    if thoi_gian_song is None:
        thoi_gian_song = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    het_han = datetime.now(timezone.utc) + thoi_gian_song
    du_lieu["exp"] = het_han

    return jwt.encode(
        du_lieu,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================
# LAY USER HIEN TAI
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token khong hop le hoac da het han",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    nguoi_dung = (
        db.query(models.NguoiDung)
        .filter(models.NguoiDung.id == user_id)
        .first()
    )

    if nguoi_dung is None:
        raise credentials_exception

    return nguoi_dung


# =========================
# KIEM TRA VAI TRO
# =========================

VAI_TRO_HOP_LE = {"thu_kho", "ke_toan"}


def yeu_cau_vai_tro(*cac_vai_tro: str):
    vai_tro_khong_hop_le = set(cac_vai_tro) - VAI_TRO_HOP_LE

    if vai_tro_khong_hop_le:
        raise ValueError(
            f"Vai tro khong hop le: {vai_tro_khong_hop_le}"
        )

    def kiem_tra_vai_tro(
        nguoi_dung=Depends(get_current_user)
    ):
        if nguoi_dung.vai_tro not in cac_vai_tro:
            raise HTTPException(
                status_code=403,
                detail="Ban khong co quyen thuc hien thao tac nay"
            )

        return nguoi_dung

    return kiem_tra_vai_tro