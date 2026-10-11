from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import io
import os
import tempfile

from app.database import SessionLocal
from app import crud, models
from app.nhap_xuat import doc_csv


router = APIRouter(
    prefix="/nhap-xuat",
    tags=["Nhap Xuat"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/hang-hoa.csv")
async def nhap_hang_hoa_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    noi_dung = await file.read()

    try:
        # Tạo file tạm
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        ) as file_tam:
            file_tam.write(noi_dung)
            duong_dan = file_tam.name

        # Đọc và kiểm tra CSV
        du_lieu, loi = doc_csv(duong_dan)

        so_luong_them = 0

        # Thêm từng hàng hóa hợp lệ vào database
        for dong in du_lieu:

            hang_hoa_cu = (
                db.query(models.HangHoa)
                .filter(
                    models.HangHoa.ma_hang == dong["ma_hang"]
                )
                .first()
            )

            # Nếu mã hàng đã tồn tại
            if hang_hoa_cu is not None:
                loi.append({
                    "ma_hang": dong["ma_hang"],
                    "ly_do": "Ma hang da ton tai trong database"
                })
                continue

            hang_hoa_moi = models.HangHoa(
                ma_hang=dong["ma_hang"],
                ten_hang=dong.get("ten_hang", ""),
                nhom=dong.get("nhom", ""),
                don_vi_tinh=dong.get("don_vi_tinh", ""),
                ton_kho=0,
                ton_toi_thieu=0,
                gia_von=0
            )

            db.add(hang_hoa_moi)
            so_luong_them += 1

        db.commit()

        return {
            "so_luong_them": so_luong_them,
            "du_lieu": du_lieu,
            "loi": loi
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=f"Khong nhap duoc file CSV: {str(e)}"
        )

    finally:
        if "duong_dan" in locals() and os.path.exists(duong_dan):
            os.remove(duong_dan)

# =========================
# XUẤT TỒN KHO CSV
# =========================

@router.get("/ton-kho.csv")
def xuat_ton_kho_csv(
    db: Session = Depends(get_db)
):
    hang_hoa = crud.lay_danh_sach_hang_hoa(
        db,
        None,
        0,
        10000
    )

    noi_dung = (
        "ma_hang,ten_hang,nhom,don_vi_tinh,"
        "ton_kho,ton_toi_thieu,gia_von\n"
    )

    for hang in hang_hoa:
        noi_dung += (
            f"{hang.ma_hang},"
            f"{hang.ten_hang},"
            f"{hang.nhom},"
            f"{hang.don_vi_tinh},"
            f"{hang.ton_kho},"
            f"{hang.ton_toi_thieu},"
            f"{hang.gia_von}\n"
        )

    return StreamingResponse(
        io.BytesIO(noi_dung.encode("utf-8")),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=ton-kho.csv"
        }
    )


# =========================
# XUẤT BÁO CÁO JSON
# =========================

@router.get("/bao-cao.json")
def xuat_bao_cao_json(
    db: Session = Depends(get_db)
):
    hang_hoa = crud.lay_danh_sach_hang_hoa(
        db,
        None,
        0,
        10000
    )

    bao_cao = []

    for hang in hang_hoa:
        bao_cao.append({
            "ma_hang": hang.ma_hang,
            "ten_hang": hang.ten_hang,
            "nhom": hang.nhom,
            "ton_kho": hang.ton_kho,
            "ton_toi_thieu": hang.ton_toi_thieu,
            "gia_von": hang.gia_von
        })

    return {
        "tong_so_hang_hoa": len(bao_cao),
        "du_lieu": bao_cao
    }