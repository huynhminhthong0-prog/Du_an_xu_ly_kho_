# Dự án cuối khóa — API Quản lý kho hàng

## 1. Giới thiệu

**API Quản lý kho hàng** là dự án xây dựng hệ thống quản lý nhập, xuất và tồn kho cho cửa hàng vật liệu.

Hệ thống được phát triển bằng Python và FastAPI, sử dụng SQLAlchemy để làm việc với cơ sở dữ liệu SQLite. Dự án áp dụng phân quyền người dùng, xác thực bằng JWT và tổ chức mã nguồn theo các module chức năng.

Mục tiêu của dự án là quản lý hàng hóa, kiểm soát quy trình nhập xuất và đảm bảo số lượng tồn kho được cập nhật theo đúng nghiệp vụ.

## 2. Chức năng chính

### 2.1. Quản lý hàng hóa

* Xem danh sách hàng hóa và thông tin chi tiết.
* Quản lý mã hàng, tên hàng, nhóm hàng và đơn vị tính.
* Theo dõi số lượng tồn kho và mức tồn kho tối thiểu.
* Quản lý giá vốn của hàng hóa.

### 2.2. Quản lý nhà cung cấp

* Quản lý thông tin nhà cung cấp.
* Lưu mã nhà cung cấp, tên nhà cung cấp và số điện thoại.
* Liên kết nhà cung cấp với phiếu nhập kho.

### 2.3. Quản lý phiếu nhập và phiếu xuất

* Tạo phiếu nhập hoặc phiếu xuất.
* Thêm, xem, chỉnh sửa và xóa các dòng hàng theo trạng thái phiếu và quyền người dùng.
* Lưu số lượng và đơn giá của từng mặt hàng.
* Kiểm tra và khóa phiếu theo quy trình nghiệp vụ.

### 2.4. Quản lý người dùng và phân quyền

Hệ thống có hai vai trò chính:

**Thủ kho (`thu_kho`)**

* Xem hàng hóa và thông tin phiếu.
* Tạo phiếu nhập, phiếu xuất.
* Thêm và chỉnh sửa các dòng hàng trong phiếu chưa khóa.
* Thực hiện các thao tác nghiệp vụ được phân quyền.

**Kế toán (`ke_toan`)**

* Xem hàng hóa và thông tin phiếu.
* Kiểm tra và khóa phiếu.
* Xem báo cáo phục vụ theo dõi tình hình tồn kho.

Hệ thống sử dụng JWT để xác thực người dùng và kiểm soát quyền truy cập API.

### 2.5. Nhập xuất dữ liệu và báo cáo

* Hỗ trợ các chức năng nhập xuất dữ liệu CSV theo API được triển khai.
* Theo dõi tồn kho.
* Xem báo cáo hàng hóa và các thông tin tồn kho theo chức năng báo cáo của hệ thống.

## 3. Công nghệ sử dụng

| Công nghệ  | Vai trò                                  |
| ---------- | ---------------------------------------- |
| Python     | Ngôn ngữ lập trình chính                 |
| FastAPI    | Xây dựng REST API                        |
| SQLAlchemy | ORM và thao tác cơ sở dữ liệu            |
| SQLite     | Lưu trữ dữ liệu                          |
| Alembic    | Quản lý phiên bản cấu trúc cơ sở dữ liệu |
| Pydantic   | Kiểm tra và xác thực dữ liệu đầu vào     |
| JWT        | Xác thực người dùng                      |
| bcrypt     | Băm mật khẩu                             |
| CSV        | Trao đổi dữ liệu                         |
| Swagger UI | Kiểm thử và tài liệu API                 |

## 4. Quy trình nghiệp vụ

Quy trình nhập kho cơ bản:

1. Thủ kho đăng nhập vào hệ thống.
2. Thủ kho tạo phiếu nhập.
3. Thủ kho thêm các mặt hàng, số lượng và đơn giá.
4. Thủ kho kiểm tra, chỉnh sửa các dòng hàng khi phiếu chưa khóa.
5. Kế toán đăng nhập và kiểm tra phiếu.
6. Kế toán khóa phiếu.
7. Hệ thống cập nhật tồn kho sau khi khóa phiếu thành công.
8. Kế toán theo dõi số lượng tồn kho và xem báo cáo.

Quy trình xuất kho được thực hiện tương tự, nhưng hệ thống phải kiểm tra lượng tồn trước khi cho phép xuất hàng.

## 5. Các quy tắc nghiệp vụ quan trọng

### Quy tắc 1: Không xuất vượt tồn kho

Nếu số lượng xuất vượt quá số lượng tồn kho hiện tại, hệ thống từ chối thao tác và trả về HTTP `409 Conflict`.

### Quy tắc 2: Không chỉnh sửa phiếu đã khóa

Phiếu đã khóa không được chỉnh sửa, thêm dòng hàng, xóa dòng hàng hoặc khóa lại. Các thao tác không hợp lệ trả về HTTP `409 Conflict`.

### Quy tắc 3: Không khóa phiếu rỗng

Phiếu chưa có dòng hàng không được phép khóa. Hệ thống trả về HTTP `409 Conflict`.

### Quy tắc 4: Phiếu nhập phải có nhà cung cấp

Phiếu nhập không có nhà cung cấp hợp lệ sẽ không được khóa và trả về HTTP `409 Conflict`.

### Quy tắc 5: Chỉ cập nhật tồn kho khi khóa phiếu

Tồn kho chỉ được thay đổi khi phiếu được khóa thành công. Quá trình xử lý phải kiểm tra các điều kiện nghiệp vụ trước khi cập nhật dữ liệu để tránh cập nhật dở dang khi xảy ra lỗi.

## 6. Thiết kế cơ sở dữ liệu

Hệ thống sử dụng 5 bảng nghiệp vụ chính.

### 6.1. Bảng `hang_hoa`

Lưu thông tin hàng hóa, bao gồm:

* `id`: Khóa chính.
* `ma_hang`: Mã hàng.
* `ten_hang`: Tên hàng.
* `nhom`: Nhóm hàng.
* `don_vi_tinh`: Đơn vị tính.
* `ton_kho`: Số lượng tồn kho.
* `ton_toi_min`: Mức tồn kho tối thiểu.
* `gia_von`: Giá vốn.

### 6.2. Bảng `nha_cung_cap`

Lưu thông tin nhà cung cấp:

* `id`: Khóa chính.
* `ma_ncc`: Mã nhà cung cấp.
* `ten_ncc`: Tên nhà cung cấp.
* `dien_thoai`: Số điện thoại.

### 6.3. Bảng `nguoi_dung`

Lưu thông tin tài khoản:

* `id`: Khóa chính.
* `ten_dang_nhap`: Tên đăng nhập.
* `mat_khau_bam`: Mật khẩu đã được băm.
* `vai_tro`: Vai trò của người dùng.

### 6.4. Bảng `phieu`

Lưu thông tin phiếu nhập và phiếu xuất:

* `id`: Khóa chính.
* `ma_phieu`: Mã phiếu.
* `loai`: Loại phiếu (`nhap` hoặc `xuat`).
* `nha_cung_cap_id`: Khóa ngoại đến `nha_cung_cap.id`.
* `nguoi_tao_id`: Khóa ngoại đến `nguoi_dung.id`.
* `ngay`: Ngày lập phiếu.
* `da_khoa`: Trạng thái khóa phiếu.

### 6.5. Bảng `chi_tiet_phieu`

Lưu danh sách hàng hóa trong từng phiếu:

* `id`: Khóa chính.
* `phieu_id`: Khóa ngoại đến `phieu.id`.
* `hang_hoa_id`: Khóa ngoại đến `hang_hoa.id`.
* `so_luong`: Số lượng hàng.
* `don_gia`: Đơn giá.

### Quan hệ giữa các bảng

* Một người dùng có thể tạo nhiều phiếu.
* Một nhà cung cấp có thể liên kết với nhiều phiếu.
* Một phiếu có thể có nhiều dòng hàng.
* Một mặt hàng có thể xuất hiện trong nhiều dòng hàng thuộc các phiếu khác nhau.

## 7. Cấu trúc dự án

```text
Project_CUOI_KHOA/
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── nghiep_vu.py
│   ├── nhap_xuat.py
│   ├── seed.py
│   └── routers/
│       ├── auth.py
│       ├── hang_hoa.py
│       ├── nha_cung_cap.py
│       ├── nguoi_dung.py
│       ├── phieu.py
│       ├── nhap_xuat.py
│       └── thong_ke.py
├── alembic/
│   ├── env.py
│   └── versions/
├── tests/
├── alembic.ini
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 8. Cài đặt và chạy dự án

### Yêu cầu

* Python đã được cài đặt.
* pip để cài đặt các thư viện Python.

### Bước 1: Tạo môi trường ảo

Mở terminal tại thư mục dự án:

```powershell
py -m venv .venv
```

Kích hoạt môi trường ảo trên Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Bước 2: Cài đặt thư viện

```powershell
python -m pip install -r requirements.txt
```

### Bước 3: Cấu hình môi trường

Thiết lập các biến môi trường cần thiết theo cấu hình của dự án. Không đưa khóa bí mật hoặc thông tin nhạy cảm vào GitHub.

### Bước 4: Khởi chạy API

Tại thư mục gốc dự án, chạy:

```powershell
python -m fastapi dev app/main.py
```

### Bước 5: Truy cập Swagger UI

Sau khi API khởi động thành công, mở trình duyệt tại:

* Swagger UI: http://127.0.0.1:8000/docs
* OpenAPI JSON: http://127.0.0.1:8000/openapi.json

Tại Swagger UI, có thể xem danh sách endpoint, gửi yêu cầu HTTP và kiểm tra kết quả trả về.

## 9. Xác thực và kiểm thử API

1. Gọi endpoint đăng nhập `POST /auth/login` bằng tài khoản hợp lệ đã được tạo trong hệ thống.
2. Sử dụng chức năng **Authorize** trên Swagger UI để xác thực.
3. Kiểm tra thông tin người dùng bằng `GET /auth/me`.
4. Thử các API theo quyền của từng vai trò.
5. Kiểm tra các tình huống nghiệp vụ hợp lệ và không hợp lệ, đặc biệt là xuất vượt tồn, khóa phiếu rỗng và chỉnh sửa phiếu đã khóa.

Tài khoản thử nghiệm phụ thuộc vào dữ liệu được khởi tạo trong database. Không sử dụng mật khẩu mặc định hoặc tài khoản thử nghiệm cho môi trường thực tế.

## 10. Quản lý cơ sở dữ liệu

Dự án sử dụng SQLite với file database `kho_hang.db`.

Các file database và file sao lưu chỉ phục vụ phát triển, thử nghiệm hoặc lưu trữ nội bộ; không nên đưa chúng lên repository công khai nếu chứa dữ liệu thực tế.

Dự án có sử dụng Alembic để quản lý migration. Khi thay đổi model, cần tạo và kiểm tra migration trước khi áp dụng lên database. Revision migration ban đầu hiện tại chỉ ghi nhận trạng thái của database có sẵn, vì vậy cần xây dựng migration đầy đủ nếu triển khai trên một database mới.

## 11. Hướng phát triển

* Bổ sung bộ kiểm thử tự động cho các API và quy tắc nghiệp vụ.
* Hoàn thiện migration để khởi tạo database mới từ đầu.
* Bổ sung kiểm tra dữ liệu đầu vào và các ràng buộc toàn vẹn.
* Hoàn thiện báo cáo tồn kho và cảnh báo hàng dưới mức tồn tối thiểu.
* Bổ sung logging và xử lý lỗi thống nhất.
* Triển khai hệ thống trên môi trường máy chủ phù hợp.

---

**Dự án cuối khóa — API Quản lý kho hàng**

Công nghệ chính: Python, FastAPI, SQLAlchemy, SQLite và Alembic.
