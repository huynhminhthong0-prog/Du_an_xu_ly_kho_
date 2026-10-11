from abc import ABC, abstractmethod


class LoaiPhieu(ABC):
    """Moi loai phieu tu biet luat cua minh."""

    @abstractmethod
    def kiem_tra_dong(self, hang_hoa, so_luong) -> str | None:
        ...

    @abstractmethod
    def ap_dung_ton_kho(self, ton_hien_tai: int, so_luong: int) -> int:
        ...

    @abstractmethod
    def bat_buoc_nha_cung_cap(self) -> bool:
        ...


class PhieuNhap(LoaiPhieu):
    def kiem_tra_dong(self, hang_hoa, so_luong):
        if so_luong <=0:
            return "So luong phai lon hon 0"
        return None
    def ap_dung_ton_kho(self, ton_hien_tai, so_luong):
        return ton_hien_tai +so_luong
    def bat_buoc_nha_cung_cap(self):
        return True



class PhieuXuat(LoaiPhieu):
    def kiem_tra_dong(self, hang_hoa, so_luong):
        if so_luong <= 0:
            return "So luong phai lon hon 0"

        if so_luong > hang_hoa.ton_kho:
            return "Khong du ton kho"

        return None
    def ap_dung_ton_kho(self, ton_hien_tai, so_luong):
        return  ton_hien_tai -so_luong
    def bat_buoc_nha_cung_cap(self):
        return False


def lay_loai(ten: str) -> LoaiPhieu:
    """'nhap' -> PhieuNhap(), 'xuat' -> PhieuXuat(). Day la cho DUY NHAT co if."""
    if ten == "nhap":
        return PhieuNhap()
    if ten == "xuat":
        return PhieuXuat()
    raise ValueError("Loai phieu khong hop le")


class CachTinhGiaVon(ABC):
    @abstractmethod
    def tinh(self, gia_von_cu, ton_cu, gia_nhap, so_luong_nhap) -> float: 
        ...

class LayGiaNhapGanNhat(CachTinhGiaVon): 
    def tinh(self, gia_von_cu, ton_cu, gia_nhap, so_luong_nhap):
        return  gia_nhap

class BinhQuanGiaQuyen(CachTinhGiaVon): 
    def tinh(self, gia_von_cu, ton_cu, gia_nhap, so_luong_nhap):
        tong_gia_tri=(gia_von_cu*ton_cu)+(gia_nhap*so_luong_nhap)
        tong_so_luong = ton_cu + so_luong_nhap
        if tong_so_luong ==0:
            return 0
        return  tong_gia_tri/ tong_so_luong