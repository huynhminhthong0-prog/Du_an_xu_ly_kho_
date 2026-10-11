from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal
from app.schemas import (
    NhaCungCapCreate,
    NhaCungCapResponse
)


router = APIRouter(
    prefix="/nha-cung-cap",
    tags=["Nha Cung Cap"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=NhaCungCapResponse,
    status_code=201
)
def tao_nha_cung_cap(
    nha_cung_cap: NhaCungCapCreate,
    db: Session = Depends(get_db)
):
    return crud.tao_nha_cung_cap(
        db,
        nha_cung_cap
    )


@router.get(
    "",
    response_model=list[NhaCungCapResponse]
)
def lay_danh_sach_nha_cung_cap(
    bo_qua: int = 0,
    gioi_han: int = 20,
    db: Session = Depends(get_db)
):
    return crud.lay_danh_sach_nha_cung_cap(
        db,
        bo_qua,
        gioi_han
    )


@router.get(
    "/{nha_cung_cap_id}",
    response_model=NhaCungCapResponse
)
def lay_nha_cung_cap(
    nha_cung_cap_id: int,
    db: Session = Depends(get_db)
):
    nha_cung_cap = crud.lay_nha_cung_cap(
        db,
        nha_cung_cap_id
    )

    if nha_cung_cap is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay nha cung cap"
        )

    return nha_cung_cap


@router.put(
    "/{nha_cung_cap_id}",
    response_model=NhaCungCapResponse
)
def cap_nhat_nha_cung_cap(
    nha_cung_cap_id: int,
    nha_cung_cap: NhaCungCapCreate,
    db: Session = Depends(get_db)
):
    nha_cung_cap_cap_nhat = crud.cap_nhat_nha_cung_cap(
        db,
        nha_cung_cap_id,
        nha_cung_cap
    )

    if nha_cung_cap_cap_nhat is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay nha cung cap"
        )

    return nha_cung_cap_cap_nhat


@router.delete(
    "/{nha_cung_cap_id}",
    status_code=204
)
def xoa_nha_cung_cap(
    nha_cung_cap_id: int,
    db: Session = Depends(get_db)
):
    nha_cung_cap = crud.xoa_nha_cung_cap(
        db,
        nha_cung_cap_id
    )

    if nha_cung_cap is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay nha cung cap"
        )