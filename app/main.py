from fastapi import FastAPI

from app.database import tao_database

from app.routers import (
    hang_hoa,
    nha_cung_cap,
    phieu,
    nguoi_dung,
    nhap_xuat,
    thong_ke,
    auth
)
tao_database()


app = FastAPI(
    title="API Quan Ly Kho Hang"
)


app.include_router(hang_hoa.router)
app.include_router(nha_cung_cap.router)
app.include_router(phieu.router)
app.include_router(nguoi_dung.router)
app.include_router(nhap_xuat.router)
app.include_router(thong_ke.router)
app.include_router(auth.router)


@app.get("/ping", tags=["He thong"])
async def ping():
    return {"status": "ok"}