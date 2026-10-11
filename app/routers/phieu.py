
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal
from app.auth import get_current_user, yeu_cau_vai_tro
from app.schemas import (
    PhieuCreate,
    PhieuResponse,
    ChiTietPhieuCreate,
    ChiTietPhieuResponse
)

router = APIRouter(
    prefix="/phieu",
    tags=["Phieu"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# TAO PHIEU - THU KHO
# =========================

@router.post(
    "",
    response_model=PhieuResponse,
    status_code=201
)
def tao_phieu(
    phieu: PhieuCreate,
    db: Session = Depends(get_db),
    nguoi_dung=Depends(yeu_cau_vai_tro("thu_kho"))
):
    return crud.tao_phieu(db, phieu)


# =========================
# DANH SACH PHIEU
# =========================

@router.get(
    "",
    response_model=list[PhieuResponse]
)
def lay_danh_sach_phieu(
    bo_qua: int = 0,
    gioi_han: int = 20,
    db: Session = Depends(get_db),
    nguoi_dung=Depends(get_current_user)
):
    return crud.lay_danh_sach_phieu(
        db,
        bo_qua,
        gioi_han
    )


# =========================
# CHI TIET MOT PHIEU
# =========================

@router.get(
    "/{phieu_id}",
    response_model=PhieuResponse
)
def lay_phieu(
    phieu_id: int,
    db: Session = Depends(get_db),
    nguoi_dung=Depends(get_current_user)
):
    phieu = crud.lay_phieu(db, phieu_id)

    if phieu is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay phieu"
        )

    return phieu


# =========================
# SUA PHIEU - THU KHO
# =========================

@router.put(
    "/{phieu_id}",
    response_model=PhieuResponse
)
def cap_nhat_phieu(
    phieu_id: int,
    phieu: PhieuCreate,
    db: Session = Depends(get_db),
    nguoi_dung=Depends(yeu_cau_vai_tro("thu_kho"))
):
    phieu_cap_nhat, loi = crud.cap_nhat_phieu(
        db,
        phieu_id,
        phieu
    )

    if loi is not None:
        if loi == "Khong tim thay phieu":
            raise HTTPException(status_code=404, detail=loi)

        raise HTTPException(status_code=409, detail=loi)

    return phieu_cap_nhat


# =========================
# XOA PHIEU - THU KHO
# =========================

@router.delete(
    "/{phieu_id}",
    status_code=204
)
def xoa_phieu(
    phieu_id: int,
    db: Session = Depends(get_db),
    nguoi_dung=Depends(yeu_cau_vai_tro("thu_kho"))
):
    phieu, loi = crud.xoa_phieu(db, phieu_id)

    if loi is not None:
        if loi == "Khong tim thay phieu":
            raise HTTPException(status_code=404, detail=loi)

        raise HTTPException(status_code=409, detail=loi)


# =========================
# THEM DONG PHIEU - THU KHO
# =========================

@router.post(
    "/{phieu_id}/dong",
    response_model=ChiTietPhieuResponse,
    status_code=201
)
def them_dong_phieu(
    phieu_id: int,
    chi_tiet: ChiTietPhieuCreate,
    db: Session = Depends(get_db),
    nguoi_dung=Depends(yeu_cau_vai_tro("thu_kho"))
):
    dong_moi, loi = crud.tao_chi_tiet_phieu(
        db,
        phieu_id,
        chi_tiet
    )

    if loi is not None:
        if loi == "Khong tim thay phieu":
            raise HTTPException(status_code=404, detail=loi)

        raise HTTPException(status_code=409, detail=loi)

    return dong_moi


# =========================
# XEM CAC DONG PHIEU
# =========================

@router.get(
    "/{phieu_id}/dong",
    response_model=list[ChiTietPhieuResponse]
)
def lay_danh_sach_dong(
    phieu_id: int,
    db: Session = Depends(get_db),
    nguoi_dung=Depends(get_current_user)
):
    phieu = crud.lay_phieu(db, phieu_id)

    if phieu is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay phieu"
        )

    return crud.lay_danh_sach_chi_tiet_phieu(
        db,
        phieu_id
    )


# =========================
# XOA DONG PHIEU - THU KHO
# =========================

@router.delete(
    "/{phieu_id}/dong/{dong_id}",
    status_code=204
)
def xoa_dong_phieu(
    phieu_id: int,
    dong_id: int,
    db: Session = Depends(get_db),
    nguoi_dung=Depends(yeu_cau_vai_tro("thu_kho"))
):
    dong, loi = crud.xoa_chi_tiet_phieu(
        db,
        phieu_id,
        dong_id
    )

    if loi is not None:
        if loi in [
            "Khong tim thay phieu",
            "Khong tim thay dong phieu"
        ]:
            raise HTTPException(status_code=404, detail=loi)

        raise HTTPException(status_code=409, detail=loi)


# =========================
# KHOA PHIEU - KE TOAN
# =========================

@router.post(
    "/{phieu_id}/khoa",
    response_model=PhieuResponse
)
def khoa_phieu(
    phieu_id: int,
    db: Session = Depends(get_db),
    nguoi_dung=Depends(yeu_cau_vai_tro("ke_toan"))
):
    phieu, loi = crud.khoa_phieu(db, phieu_id)

    if loi is not None:
        if loi == "Khong tim thay phieu":
            raise HTTPException(status_code=404, detail=loi)

        raise HTTPException(status_code=409, detail=loi)

    return phieu