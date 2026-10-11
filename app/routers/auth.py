
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models
from app.auth import (
    kiem_tra_mat_khau,
    tao_access_token,
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def dang_nhap(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    nguoi_dung = (
        db.query(models.NguoiDung)
        .filter(
            models.NguoiDung.ten_dang_nhap == form_data.username
        )
        .first()
    )

    if nguoi_dung is None or not kiem_tra_mat_khau(
        form_data.password,
        nguoi_dung.mat_khau_bam
    ):
        raise HTTPException(
            status_code=401,
            detail="Ten dang nhap hoac mat khau khong dung",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = tao_access_token({
        "sub": str(nguoi_dung.id),
        "vai_tro": nguoi_dung.vai_tro
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def xem_toi(
    nguoi_dung=Depends(get_current_user)
):
    return {
        "id": nguoi_dung.id,
        "ten_dang_nhap": nguoi_dung.ten_dang_nhap,
        "vai_tro": nguoi_dung.vai_tro
    }