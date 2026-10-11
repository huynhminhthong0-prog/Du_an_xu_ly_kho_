import csv
import json

def doc_csv(duong_dan: str):
    du_lieu = []
    loi = []
    ma_da_co = set()

    try:
        try:
            file = open(
                duong_dan,
                "r",
                encoding="utf-8",
                newline=""
            )
        except UnicodeDecodeError:
            file = open(
                duong_dan,
                "r",
                encoding="latin-1",
                newline=""
            )

        with file:
            reader = csv.DictReader(file)

            for so_dong, dong in enumerate(reader, start=2):

                if not any(dong.values()):
                    continue

                try:
                    dong_hop_le, ly_do = kiem_tra_dong(
                        dong,
                        ma_da_co
                    )

                    if dong_hop_le is None:
                        loi.append({
                            "dong": so_dong,
                            "ly_do": ly_do
                        })
                        continue

                    du_lieu.append(dong_hop_le)
                    ma_da_co.add(dong_hop_le["ma_hang"])

                except Exception as e:
                    loi.append({
                        "dong": so_dong,
                        "ly_do": str(e)
                    })

    except Exception as e:
        loi.append({
            "dong": 0,
            "ly_do": f"Khong the doc file: {e}"
        })

    return du_lieu, loi



def chuan_hoa_so(gia_tri: str):
    gia_tri = gia_tri.strip()

    if gia_tri == "":
        return None

    if "." in gia_tri and "," in gia_tri:
        gia_tri = gia_tri.replace(".", "")
        gia_tri = gia_tri.replace(",", ".")

    elif "," in gia_tri:
        gia_tri = gia_tri.replace(",", ".")

    elif "." in gia_tri:
        phan_sau = gia_tri.split(".")[-1]

        if len(phan_sau) == 3:
            gia_tri = gia_tri.replace(".", "")

    return float(gia_tri)

def kiem_tra_dong(dong:dict,ma_da_co:set):
    ma_hang=dong.get("ma_hang","").strip()
    so_luong=dong.get("so_luong","").strip()

    if ma_hang =="":
        return None,"Thieu ma_hang"
    if ma_hang in ma_da_co:
        return None,"Ma hang bi trung"
    if so_luong=="":
        return None,"Thieu so_luong"
    try:
        so_luong= chuan_hoa_so(so_luong)
    except ValueError:
        return None,"So luong khong hop le"

    if so_luong <=0:
        return None,"So luong phai hon 0"
    dong["ma_hang"]=ma_hang
    dong["so_luong"]=so_luong
    return dong,None

def xuat_csv(duong_dan:str,du_lieu:list[dict]):
    if not du_lieu:
        return
    ten_cot=du_lieu[0].keys()
    with open (duong_dan,"w",encoding="utf-8",newline="") as file:
        writer =csv.DictWriter(file,fieldnames=ten_cot)
        writer.writeheader()
        writer.writerows(du_lieu)


def xuat_json(duong_dan:str,du_lieu):
    with open(duong_dan,"w",encoding="utf-8") as file:
        json.dump(du_lieu,file,ensure_ascii=False,indent=4)
        