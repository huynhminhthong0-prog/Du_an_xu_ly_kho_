from pydantic import BaseModel, Field

#HangHoa
class HangHoaBase(BaseModel):
    ma_hang: str = Field(min_length=1, max_length=50)
    ten_hang: str = Field(min_length=1, max_length=255)
    nhom: str = Field(min_length=1, max_length=100)
    don_vi_tinh: str = Field(min_length=1, max_length=30)
    ton_toi_thieu: int = Field(default=0, ge=0)
    gia_von: float = Field(default=0, ge=0)


class HangHoaCreate(HangHoaBase):
    pass


class HangHoaResponse(HangHoaBase):
    id: int
    ton_kho: int





#NhaCungCap
class NhaCungCapBase(BaseModel):
    ma_ncc: str = Field(min_length=1, max_length=50)
    ten_ncc: str = Field(min_length=1, max_length=100)
    dien_thoai: str | None = Field(default=None, max_length=20)


class NhaCungCapCreate(NhaCungCapBase):
    pass


class NhaCungCapResponse(NhaCungCapBase):
    id: int


#NguoiDung
class NguoiDungBase(BaseModel):
    ten_dang_nhap:str =Field(min_length=1,max_length=50)
    vai_tro:str=Field(min_length=1,max_length=100)

class NguoiDungCreate(NguoiDungBase):
    mat_khau:str=Field(min_length=1,max_length=50)


class NguoiDungResponse(NguoiDungBase):
    id:int


# Phieu

class PhieuBase(BaseModel):
    ma_phieu: str = Field(min_length=1, max_length=50)
    loai: str = Field(min_length=1, max_length=10)
    nha_cung_cap_id: int | None = None
    ngay: str = Field(min_length=1, max_length=20)


class PhieuCreate(PhieuBase):
    pass


class PhieuResponse(PhieuBase):
    id: int
    da_khoa: bool
    nguoi_tao_id: int


    

# ChiTietPhieu

class ChiTietPhieuBase(BaseModel):
    hang_hoa_id: int
    so_luong: int = Field(gt=0)
    don_gia: float = Field(ge=0)


class ChiTietPhieuCreate(ChiTietPhieuBase):
    pass


class ChiTietPhieuResponse(ChiTietPhieuBase):
    id: int
    phieu_id: int


    

