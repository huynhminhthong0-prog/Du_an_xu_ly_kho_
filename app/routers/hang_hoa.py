from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal
from app.schemas import HangHoaCreate, HangHoaResponse


router = APIRouter(
    prefix="/hang-hoa",
    tags=["Hang Hoa"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=HangHoaResponse,
    status_code=201
)
def tao_hang_hoa(
    hang_hoa: HangHoaCreate,
    db: Session = Depends(get_db)
):
    return crud.tao_hang_hoa(db, hang_hoa)


@router.get(
    "",
    response_model=list[HangHoaResponse]
)
def lay_danh_sach_hang_hoa(
    tim: str | None = None,
    bo_qua: int = 0,
    gioi_han: int = 20,
    db: Session = Depends(get_db)
):
    return crud.lay_danh_sach_hang_hoa(
        db,
        tim,
        bo_qua,
        gioi_han
    )


@router.get(
    "/{hang_hoa_id}",
    response_model=HangHoaResponse
)
def lay_hang_hoa(
    hang_hoa_id: int,
    db: Session = Depends(get_db)
):
    hang_hoa = crud.lay_hang_hoa(
        db,
        hang_hoa_id
    )

    if hang_hoa is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay hang hoa"
        )

    return hang_hoa


@router.put(
    "/{hang_hoa_id}",
    response_model=HangHoaResponse
)
def cap_nhat_hang_hoa(
    hang_hoa_id: int,
    hang_hoa: HangHoaCreate,
    db: Session = Depends(get_db)
):
    hang_hoa_cap_nhat = crud.cap_nhat_hang_hoa(
        db,
        hang_hoa_id,
        hang_hoa
    )

    if hang_hoa_cap_nhat is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay hang hoa"
        )

    return hang_hoa_cap_nhat


@router.delete(
    "/{hang_hoa_id",
    status_code=204
)
def xoa_hang_hoa(
    hang_hoa_id: int,
    db: Session = Depends(get_db)):
    hang_hoa = crud.xoa_hang_hoa(
        db,
        hang_hoa_id
    )

    if hang_hoa is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay hang hoa"
        )