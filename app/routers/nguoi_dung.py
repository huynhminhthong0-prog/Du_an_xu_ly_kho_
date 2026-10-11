from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal
from app.schemas import (
    NguoiDungCreate,
    NguoiDungResponse
)
from app.auth import bam_mat_khau


router = APIRouter(
    prefix="/nguoi-dung",
    tags=["Nguoi Dung"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=NguoiDungResponse,
    status_code=201
)
def tao_nguoi_dung(
    nguoi_dung: NguoiDungCreate,
    db: Session = Depends(get_db)
):
    mat_khau_bam = bam_mat_khau(
        nguoi_dung.mat_khau
    )
    return crud.tao_nguoi_dung(
        db,
        nguoi_dung,
        mat_khau_bam
    )


@router.get(
    "",
    response_model=list[NguoiDungResponse]
)
def lay_danh_sach_nguoi_dung(
    bo_qua: int = 0,
    gioi_han: int = 20,
    db: Session = Depends(get_db)
):
    return crud.lay_danh_sach_nguoi_dung(
        db,
        bo_qua,
        gioi_han
    )



@router.get(
    "/{nguoi_dung_id}",
    response_model=NguoiDungResponse
)
def lay_nguoi_dung(
    nguoi_dung_id: int,
    db: Session = Depends(get_db)
):
    nguoi_dung = crud.lay_nguoi_dung(
        db,
        nguoi_dung_id
    )

    if nguoi_dung is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay nguoi dung"
        )
    return nguoi_dung


@router.put(
    "/{nguoi_dung_id}",
    response_model=NguoiDungResponse
)
def cap_nhat_nguoi_dung(
    nguoi_dung_id: int,
    nguoi_dung: NguoiDungCreate,
    db: Session = Depends(get_db)
):
    nguoi_dung_cap_nhat = crud.cap_nhat_nguoi_dung(
        db,
        nguoi_dung_id,
        nguoi_dung
    )

    if nguoi_dung_cap_nhat is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay nguoi dung"
        )

    return nguoi_dung_cap_nhat

@router.delete(
    "/{nguoi_dung_id}",
    status_code=204
)
def xoa_nguoi_dung(
    nguoi_dung_id: int,
    db: Session = Depends(get_db)
):
    nguoi_dung = crud.xoa_nguoi_dung(
        db,
        nguoi_dung_id
    )

    if nguoi_dung is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay nguoi dung"
        )