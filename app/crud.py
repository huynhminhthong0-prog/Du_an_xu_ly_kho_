from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.schemas import (
    HangHoaCreate,
    NhaCungCapCreate,
    NguoiDungCreate,
    PhieuCreate,
    ChiTietPhieuCreate,
)

from app.nghiep_vu import lay_loai

# =========================================================
# HANG HOA
# =========================================================

def tao_hang_hoa(
    db: Session,
    hang_hoa: HangHoaCreate
):
    hang_moi = models.HangHoa(
        ma_hang=hang_hoa.ma_hang,
        ten_hang=hang_hoa.ten_hang,
        nhom=hang_hoa.nhom,
            don_vi_tinh=hang_hoa.don_vi_tinh,
        ton_toi_thieu=hang_hoa.ton_toi_thieu,
        gia_von=hang_hoa.gia_von
    )

    db.add(hang_moi)
    db.commit()
    db.refresh(hang_moi)

    return hang_moi


def lay_hang_hoa(db: Session, hang_hoa_id: int):
    return (
        db.query(models.HangHoa)
        .filter(models.HangHoa.id == hang_hoa_id)
        .first()
    )


def lay_danh_sach_hang_hoa(
    db: Session,
    tim: str | None = None,
    bo_qua: int = 0,
    gioi_han: int = 20
):
    query = db.query(models.HangHoa)

    if tim:
        query = query.filter(
            models.HangHoa.ma_hang.contains(tim)
            | models.HangHoa.ten_hang.contains(tim)
        )

    return (
        query
        .offset(bo_qua)
        .limit(gioi_han)
        .all()
    )


def cap_nhat_hang_hoa(
    db: Session,
    hang_hoa_id: int,
    hang_hoa: HangHoaCreate
):
    hang_hien_tai = lay_hang_hoa(db, hang_hoa_id)

    if hang_hien_tai is None:
        return None

    hang_hien_tai.ma_hang = hang_hoa.ma_hang
    hang_hien_tai.ten_hang = hang_hoa.ten_hang
    hang_hien_tai.nhom = hang_hoa.nhom
    hang_hien_tai.don_vi_tinh = hang_hoa.don_vi_tinh
    hang_hien_tai.ton_toi_thieu = hang_hoa.ton_toi_thieu
    hang_hien_tai.gia_von = hang_hoa.gia_von

    db.commit()
    db.refresh(hang_hien_tai)

    return hang_hien_tai


def xoa_hang_hoa(
    db: Session,
    hang_hoa_id: int
):
    hang_hien_tai = lay_hang_hoa(db, hang_hoa_id)
    if hang_hien_tai is None:
        return None
    db.delete(hang_hien_tai)
    db.commit()
    return hang_hien_tai


# =========================================================
# NHA CUNG CAP
# =========================================================

def tao_nha_cung_cap(
    db: Session,
    nha_cung_cap: NhaCungCapCreate
):
    ncc_moi = models.NhaCungCap(
        ma_ncc=nha_cung_cap.ma_ncc,
        ten_ncc=nha_cung_cap.ten_ncc,
        dien_thoai=nha_cung_cap.dien_thoai)
    db.add(ncc_moi)
    db.commit()
    db.refresh(ncc_moi)

    return ncc_moi


def lay_nha_cung_cap(
    db: Session,
    nha_cung_cap_id: int
):
    return (
        db.query(models.NhaCungCap)
        .filter(
            models.NhaCungCap.id == nha_cung_cap_id
        )
        .first()
    )


def lay_danh_sach_nha_cung_cap(
    db: Session,
    bo_qua: int = 0,
    gioi_han: int = 20):
    return (
        db.query(models.NhaCungCap)
        .offset(bo_qua)
        .limit(gioi_han)
        .all()
    )


def cap_nhat_nha_cung_cap(
    db: Session,
    nha_cung_cap_id: int,
    nha_cung_cap: NhaCungCapCreate
):
    ncc_hien_tai = lay_nha_cung_cap(
        db,
        nha_cung_cap_id
    )

    if ncc_hien_tai is None:
        return None

    ncc_hien_tai.ma_ncc = nha_cung_cap.ma_ncc
    ncc_hien_tai.ten_ncc = nha_cung_cap.ten_ncc
    ncc_hien_tai.dien_thoai = nha_cung_cap.dien_thoai

    db.commit()
    db.refresh(ncc_hien_tai)

    return ncc_hien_tai


def xoa_nha_cung_cap(
    db: Session,
    nha_cung_cap_id: int
):
    ncc_hien_tai = lay_nha_cung_cap(
        db,
        nha_cung_cap_id
    )

    if ncc_hien_tai is None:
        return None

    db.delete(ncc_hien_tai)
    db.commit()

    return ncc_hien_tai


# =========================================================
# NGUOI DUNG
# =========================================================

def tao_nguoi_dung(
    db: Session,
    nguoi_dung: NguoiDungCreate,
    mat_khau_bam: str
):
    nguoi_dung_moi = models.NguoiDung(
        ten_dang_nhap=nguoi_dung.ten_dang_nhap,
        mat_khau_bam=mat_khau_bam,
        vai_tro=nguoi_dung.vai_tro
    )

    db.add(nguoi_dung_moi)
    db.commit()
    db.refresh(nguoi_dung_moi)

    return nguoi_dung_moi


def lay_nguoi_dung(
    db: Session,
    nguoi_dung_id: int
):
    return (
        db.query(models.NguoiDung)
        .filter(
            models.NguoiDung.id == nguoi_dung_id
        )
        .first()
    )


def lay_nguoi_dung_theo_ten_dang_nhap(
    db: Session,
    ten_dang_nhap: str
):
    return (
        db.query(models.NguoiDung)
        .filter(
            models.NguoiDung.ten_dang_nhap
            == ten_dang_nhap
        )
        .first()
    )


def lay_danh_sach_nguoi_dung(
    db: Session,
    bo_qua: int = 0,
    gioi_han: int = 20
):
    return (
        db.query(models.NguoiDung)
        .offset(bo_qua)
        .limit(gioi_han)
        .all()
    )


def cap_nhat_nguoi_dung(
    db: Session,
    nguoi_dung_id: int,
    nguoi_dung: NguoiDungCreate,
    mat_khau_bam: str | None = None
):
    nguoi_dung_hien_tai = lay_nguoi_dung(
        db,
        nguoi_dung_id
    )

    if nguoi_dung_hien_tai is None:
        return None

    nguoi_dung_hien_tai.ten_dang_nhap = (
        nguoi_dung.ten_dang_nhap
    )

    nguoi_dung_hien_tai.vai_tro = (
        nguoi_dung.vai_tro
    )

    if mat_khau_bam is not None:
        nguoi_dung_hien_tai.mat_khau_bam = mat_khau_bam

    db.commit()
    db.refresh(nguoi_dung_hien_tai)

    return nguoi_dung_hien_tai


def xoa_nguoi_dung(
    db: Session,
    nguoi_dung_id: int
):
    nguoi_dung_hien_tai = lay_nguoi_dung(
        db,
        nguoi_dung_id
    )

    if nguoi_dung_hien_tai is None:
        return None

    db.delete(nguoi_dung_hien_tai)
    db.commit()

    return nguoi_dung_hien_tai


# =========================================================
# PHIEU
# =========================================================

def tao_phieu(db, phieu):
    phieu_moi = models.Phieu(
        ma_phieu=phieu.ma_phieu,
        loai=phieu.loai,
        nha_cung_cap_id=phieu.nha_cung_cap_id,
        ngay=phieu.ngay,
        nguoi_tao_id=1
    )

    db.add(phieu_moi)
    db.commit()
    db.refresh(phieu_moi)

    return phieu_moi

def lay_phieu(
    db: Session,
    phieu_id: int
):
    return (
        db.query(models.Phieu)
        .filter(
            models.Phieu.id == phieu_id
        )
        .first()
    )


def lay_danh_sach_phieu(
    db: Session,
    bo_qua: int = 0,
    gioi_han: int = 20
):
    return (
        db.query(models.Phieu)
        .offset(bo_qua)
        .limit(gioi_han)
        .all()
    )


def cap_nhat_phieu(
    db: Session,
    phieu_id: int,
    phieu: PhieuCreate
):
    phieu_hien_tai = lay_phieu(
        db,
        phieu_id
    )

    if phieu_hien_tai is None:
        return None, "Khong tim thay phieu"

    if phieu_hien_tai.da_khoa:
        return None, "Phieu da duoc khoa"

    phieu_hien_tai.ma_phieu = phieu.ma_phieu
    phieu_hien_tai.loai = phieu.loai
    phieu_hien_tai.nha_cung_cap_id = phieu.nha_cung_cap_id
    phieu_hien_tai.ngay = phieu.ngay

    db.commit()
    db.refresh(phieu_hien_tai)

    return phieu_hien_tai, None


def xoa_phieu(db: Session, phieu_id: int):
    phieu_hien_tai = lay_phieu(db, phieu_id)

    if phieu_hien_tai is None:
        return None, "Khong tim thay phieu"

    if phieu_hien_tai.da_khoa:
        return None, "Phieu da duoc khoa"

    db.delete(phieu_hien_tai)
    db.commit()

    return phieu_hien_tai, None

# =========================================================
# CHI TIET PHIEU
# =========================================================

def tao_chi_tiet_phieu(
    db: Session,
    phieu_id: int,
    chi_tiet: ChiTietPhieuCreate
):
  
    phieu = lay_phieu(db, phieu_id)

    if phieu is None:
        return None, "Khong tim thay phieu"
    if phieu.da_khoa:
        return None, "Phieu da duoc khoa"

    hang_hoa = lay_hang_hoa(
        db,
        chi_tiet.hang_hoa_id
    )

    if hang_hoa is None:
        return None, "Khong tim thay hang hoa"

    chi_tiet_moi = models.ChiTietPhieu(
        phieu_id=phieu_id,
        hang_hoa_id=chi_tiet.hang_hoa_id,
        so_luong=chi_tiet.so_luong,
        don_gia=chi_tiet.don_gia
    )

    db.add(chi_tiet_moi)
    db.commit()
    db.refresh(chi_tiet_moi)

    return chi_tiet_moi, None


def lay_chi_tiet_phieu(
    db: Session,
    chi_tiet_id: int
):
    return (
        db.query(models.ChiTietPhieu)
        .filter(
            models.ChiTietPhieu.id == chi_tiet_id
        )
        .first()
    )


def lay_danh_sach_chi_tiet_phieu(
    db: Session,
    phieu_id: int
):
    return (
        db.query(models.ChiTietPhieu)
        .filter(
            models.ChiTietPhieu.phieu_id == phieu_id
        )
        .all()
    )


def xoa_chi_tiet_phieu(
    db: Session,
    phieu_id: int,
    chi_tiet_id: int
):
    phieu = lay_phieu(db, phieu_id)
    if phieu is None:
        return None, "Khong tim thay phieu"
    if phieu.da_khoa:
        return None, "Phieu da duoc khoa"
    chi_tiet_hien_tai = (
        db.query(models.ChiTietPhieu)
        .filter(
            models.ChiTietPhieu.id == chi_tiet_id,
            models.ChiTietPhieu.phieu_id == phieu_id
        )
        .first()
    )
    if chi_tiet_hien_tai is None:
        return None, "Khong tim thay dong phieu"
    db.delete(chi_tiet_hien_tai)
    db.commit()
    return chi_tiet_hien_tai, None


# =========================================================
# BAO CAO SQL
# =========================================================

# Hàng dưới tồn tối thiểu

def lay_hang_duoi_ton_toi_thieu(
    db: Session
):
    return (
        db.query(models.HangHoa)
        .filter(
            models.HangHoa.ton_kho
            < models.HangHoa.ton_toi_thieu
        )
        .all()
    )


# Báo cáo giá trị tồn theo nhóm
#CT:
#Giá trị tồn = ton_kho × gia_von

def lay_gia_tri_ton_theo_nhom(
    db: Session
):
    ket_qua = (
        db.query(
            models.HangHoa.nhom,
            func.sum(
                models.HangHoa.ton_kho
                * models.HangHoa.gia_von
            ).label("gia_tri_ton")
        )
        .group_by(
            models.HangHoa.nhom
        )
        .all()
    )

    return [
        {
            "nhom": nhom,
            "gia_tri_ton": gia_tri_ton
        }
        for nhom, gia_tri_ton in ket_qua
    ]


# Báo cáo hàng xuất nhiều

def lay_hang_xuat_nhieu(
    db: Session,
    tu_ngay: str,
    den_ngay: str
):
    ket_qua = (
        db.query(
            models.HangHoa.id,
            models.HangHoa.ma_hang,
            models.HangHoa.ten_hang,
            func.sum(
                models.ChiTietPhieu.so_luong
            ).label("tong_so_luong_xuat")
        )
        .join(
            models.ChiTietPhieu,
            models.ChiTietPhieu.hang_hoa_id
            == models.HangHoa.id
        )
        .join(
            models.Phieu,
            models.Phieu.id
            == models.ChiTietPhieu.phieu_id
        )
        .filter(
            models.Phieu.loai == "xuat",
            models.Phieu.ngay >= tu_ngay,
            models.Phieu.ngay <= den_ngay
        )
        .group_by(
            models.HangHoa.id,
            models.HangHoa.ma_hang,
            models.HangHoa.ten_hang
        )
        .order_by(
            func.sum(
                models.ChiTietPhieu.so_luong
            ).desc()
        )
        .all()
    )

    return [
        {
            "id": id,
            "ma_hang": ma_hang,
            "ten_hang": ten_hang,
            "tong_so_luong_xuat": tong_so_luong_xuat
        }
        for (
            id,
            ma_hang,
            ten_hang,
            tong_so_luong_xuat
        ) in ket_qua
    ]


#=======Khoa Phieu========

def khoa_phieu(
    db: Session,
    phieu_id: int
):
    phieu = lay_phieu(db, phieu_id)

    
    if phieu is None:
        return None, "Khong tim thay phieu"

    if phieu.da_khoa:
        return None, "Phieu da duoc khoa"

    cac_dong = lay_danh_sach_chi_tiet_phieu(
        db,
        phieu_id)

    if not cac_dong:
        return None, "Phieu khong co dong"

    try:
        loai_phieu = lay_loai(phieu.loai)
    except ValueError:
        return None, "Loai phieu khong hop le"
    if ( loai_phieu.bat_buoc_nha_cung_cap() and phieu.nha_cung_cap_id is None ):
        return None, "Phieu nhap bat buoc co nha cung cap"

    # =====================================================
    # GIAI DOAN 1: KIEM TRA TAT CA CAC DONG
    # =====================================================

    cac_thay_doi = []

    for dong in cac_dong:

        hang_hoa = lay_hang_hoa(
            db,
            dong.hang_hoa_id
        )

        if hang_hoa is None:
            return None, (
                f"Khong tim thay hang hoa "
                f"id={dong.hang_hoa_id}"
            )

        loi = loai_phieu.kiem_tra_dong(
            hang_hoa,
            dong.so_luong
        )

        if loi is not None:
            return None, loi


        ton_moi = loai_phieu.ap_dung_ton_kho(
            hang_hoa.ton_kho,
            dong.so_luong
        )

        cac_thay_doi.append(
            (hang_hoa, ton_moi)
        )

    # =====================================================
    # GIAI DOAN 2: AP DUNG THAY DOI
    # =====================================================

    try:

        for hang_hoa, ton_moi in cac_thay_doi:
            hang_hoa.ton_kho = ton_moi

        phieu.da_khoa = True

        db.commit()

    except Exception:
        db.rollback()
        raise

    db.refresh(phieu)

    return phieu, None