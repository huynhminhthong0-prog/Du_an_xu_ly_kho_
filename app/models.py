from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class HangHoa(Base):
    __tablename__ = "hang_hoa"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ma_hang: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    ten_hang: Mapped[str] = mapped_column(String(255), nullable=False)
    nhom: Mapped[str] = mapped_column(String(100), nullable=False)
    don_vi_tinh: Mapped[str] = mapped_column(String(30), nullable=False)  
    ton_kho: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ton_toi_thieu: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    gia_von: Mapped[float] = mapped_column(Float, default=0, nullable=False)  


class NhaCungCap(Base):
    __tablename__ = "nha_cung_cap"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ma_ncc: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    ten_ncc: Mapped[str] = mapped_column(String(100), nullable=False)
    dien_thoai: Mapped[str | None] = mapped_column(String(20), nullable=True)


class NguoiDung(Base):
    __tablename__ = "nguoi_dung"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ten_dang_nhap: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    mat_khau_bam: Mapped[str] = mapped_column(String(255), nullable=False)  
    vai_tro: Mapped[str] = mapped_column(String(20), nullable=False)


class Phieu(Base):
    __tablename__ = "phieu"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    ma_phieu: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    loai: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    nha_cung_cap_id: Mapped[int | None] = mapped_column(
        ForeignKey("nha_cung_cap.id"),
        nullable=True
    )

    ngay: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    da_khoa: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    nguoi_tao_id: Mapped[int] = mapped_column(
        ForeignKey("nguoi_dung.id"),
        nullable=False
    )

class ChiTietPhieu(Base):
    __tablename__ = "chi_tiet_phieu"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phieu_id: Mapped[int] = mapped_column(ForeignKey("phieu.id"), nullable=False)
    hang_hoa_id: Mapped[int] = mapped_column(
        ForeignKey("hang_hoa.id"), nullable=False
    )
    so_luong: Mapped[int] = mapped_column(Integer, nullable=False) 
    don_gia: Mapped[float] = mapped_column(Float, nullable=False)  