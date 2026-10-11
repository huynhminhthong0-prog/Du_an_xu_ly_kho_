from app.database import SessionLocal, tao_database
from app import models
from app.auth import bam_mat_khau


def seed_data():

    # Tạo database và các bảng
    tao_database()

    db = SessionLocal()

    try:

# ==================================
# NGƯỜI DÙNG
# ==================================

        admin = (
            db.query(models.NguoiDung)
            .filter(models.NguoiDung.ten_dang_nhap == "admin")
            .first()
        )

        if admin is None:
            admin = models.NguoiDung(
                ten_dang_nhap="admin",
                mat_khau_bam=bam_mat_khau("123456"),
                vai_tro="thu_kho"
            )
            db.add(admin)
        else:
            admin.vai_tro = "thu_kho"

        ketoan = (
            db.query(models.NguoiDung)
            .filter(models.NguoiDung.ten_dang_nhap == "ketoan")
            .first()
        )

        if ketoan is None:
            ketoan = models.NguoiDung(
                ten_dang_nhap="ketoan",
                mat_khau_bam=bam_mat_khau("123456"),
                vai_tro="ke_toan"
            )
            db.add(ketoan)
        else:
            ketoan.vai_tro = "ke_toan"

        # ==================================
        # NHÀ CUNG CẤP
        # ==================================

        if db.query(models.NhaCungCap).count() == 0:

            ncc1 = models.NhaCungCap(
                ma_ncc="NCC001",
                ten_ncc="Cong ty Vat Tu A",
                dien_thoai="0901234567"
            )

            ncc2 = models.NhaCungCap(
                ma_ncc="NCC002",
                ten_ncc="Cong ty Vat Tu B",
                dien_thoai="0907654321"
            )

            db.add_all([
                ncc1,
                ncc2
            ])

        # ==================================
        # HÀNG HÓA
        # ==================================

        if db.query(models.HangHoa).count() == 0:

            hang1 = models.HangHoa(
                ma_hang="HH001",
                ten_hang="Thep hop",
                nhom="Kim loai",
                don_vi_tinh="kg",
                ton_kho=100,
                ton_toi_thieu=20,
                gia_von=50000
            )

            hang2 = models.HangHoa(
                ma_hang="HH002",
                ten_hang="Xi mang",
                nhom="Vat lieu xay dung",
                don_vi_tinh="bao",
                ton_kho=50,
                ton_toi_thieu=10,
                gia_von=85000
            )

            hang3 = models.HangHoa(
                ma_hang="HH003",
                ten_hang="Ong nhua",
                nhom="Nhua",
                don_vi_tinh="cai",
                ton_kho=200,
                ton_toi_thieu=50,
                gia_von=30000
            )

            db.add_all([
                hang1,
                hang2,
                hang3
            ])

        # ==================================
        # LƯU DATABASE
        # ==================================

        db.commit()

        print("Seed du lieu thanh cong!")

    except Exception as e:

        db.rollback()

        print("Seed that bai:")
        print(e)

    finally:

        db.close()


if __name__ == "__main__":
    seed_data()