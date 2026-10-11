from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud


router = APIRouter(
    prefix="/thong-ke",
    tags=["Thong Ke"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================
# HÀNG DƯỚI TỒN TỐI THIỂU
# =========================

@router.get("/duoi-ton-toi-thieu")
def hang_duoi_ton_toi_thieu(
    db: Session = Depends(get_db)
):
    return crud.lay_hang_duoi_ton_toi_thieu(db)


# =========================
# GIÁ TRỊ TỒN KHO THEO NHÓM
# =========================

@router.get("/gia-tri-ton-theo-nhom")
def gia_tri_ton_theo_nhom(
    db: Session = Depends(get_db)
):
    return crud.lay_gia_tri_ton_theo_nhom(db)


# =========================
# HÀNG XUẤT NHIỀU TRONG KỲ
# =========================

@router.get("/hang-xuat-nhieu")
def hang_xuat_nhieu(
    tu_ngay: str,
    den_ngay: str,
    db: Session = Depends(get_db)
):
    return crud.lay_hang_xuat_nhieu(
        db,
        tu_ngay,
        den_ngay
    )