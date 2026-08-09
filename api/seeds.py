import asyncio
import bcrypt
from lib.cryptographic import encrypt_text
from datetime import datetime  # <-- Tambahkan ini untuk mengatasi error created_at
from prisma import Prisma

async def main() -> None:
    # Koneksi ke database sebelum melakukan query
    db = Prisma()
    await db.connect()
    
    # Menghapus data lama
    await db.ccvtv.delete_many()
    await db.profile.delete_many()
    await db.accounts.delete_many()

    bekasi_cctv = [
        {
            "camera_name": "Depan Anugrah Motor",
            "location_description": "Jl. Ir. H. Juanda, dekat bengkel Anugrah Motor",
            "category": "PUBLIC",
            "latitude": -6.234125,
            "longitude": 106.999412,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Depan_Anugrah_Motor.m3u8",
        },
        {
            "camera_name": "Depan FTL Fitness",
            "location_description": "Area pusat kebugaran FTL Fitness, jalan utama",
            "category": "PUBLIC",
            "latitude": -6.241532,
            "longitude": 106.994321,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Depan_FTL_Fitness.m3u8",
        },
        {
            "camera_name": "Depan NGOPIBAH",
            "location_description": "Area parkir dan depan kedai kopi NGOPIBAH",
            "category": "PUBLIC",
            "latitude": -6.257104,
            "longitude": 106.973415,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Depan_NGOPIBAH.m3u8",
        },
        {
            "camera_name": "Depan SMP Strada Budi Luhur",
            "location_description": "Zona selamat sekolah, Jl. Pejuang, depan gerbang SMP Strada Budi Luhur",
            "category": "PUBLIC",
            "latitude": -6.232512,
            "longitude": 107.001245,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Depan_SMP_Strada_Budi_luhur.m3u8",
        },
        {
            "camera_name": "Flyover Cipendewa",
            "location_description": "Akses jalan naik/turun jembatan layang Cipendawa",
            "category": "PUBLIC",
            "latitude": -6.291243,
            "longitude": 106.995874,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Flyover_Cipendawa.m3u8",
        },
        {
            "camera_name": "KFC dekat Taman Cut Mutia",
            "location_description": "Persimpangan dekat restoran KFC dan area hijau Taman Cut Mutia",
            "category": "PUBLIC",
            "latitude": -6.248312,
            "longitude": 107.002154,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/KFC_DEKAT_TAMAN_CUT_MUTIA.m3u8",
        },
        {
            "camera_name": "PT Fajar Mas Murni",
            "location_description": "Kawasan industri, gerbang masuk depan PT Fajar Mas Murni",
            "category": "PUBLIC",
            "latitude": -6.253612,
            "longitude": 106.968142,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/PT_Fajar_Mas_Murni.m3u8",
        },
        {
            "camera_name": "Perempatan Caman",
            "location_description": "Lampu merah persimpangan Jalan Caman Raya",
            "category": "PUBLIC",
            "latitude": -6.249814,
            "longitude": 106.957631,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Perempatan_Caman.m3u8",
        },
        {
            "camera_name": "Perempatan Rawa Semut",
            "location_description": "Traffic light persimpangan Rawa Semut, akses menuju tol East Bekasi",
            "category": "PUBLIC",
            "latitude": -6.252415,
            "longitude": 107.014523,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Perempatan_Rawa_Semut.m3u8",
        },
        {
            "camera_name": "Putaran Sumber Arta",
            "location_description": "U-turn Jalan Raya Kalimalang dekat komplek ruko Sumber Arta",
            "category": "PUBLIC",
            "latitude": -6.246712,
            "longitude": 106.942154,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Putaran_sumber_Arta.m3u8",
        },
        {
            "camera_name": "Samping RS Mitra Keluarga",
            "location_description": "Koridor jalan utama di samping Rumah Sakit Mitra Keluarga Bekasi Barat",
            "category": "PUBLIC",
            "latitude": -6.243124,
            "longitude": 106.991842,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Samping_RS_Mitra_Keluarga.m3u8",
        },
        {
            "camera_name": "Samping RS Primaya Bekasi",
            "location_description": "Jalur ambulans dan gerbang samping Rumah Sakit Primaya Bekasi",
            "category": "PUBLIC",
            "latitude": -6.244315,
            "longitude": 106.977412,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Samping_RS_Primaya_Bekasi.m3u8",
        },
        {
            "camera_name": "Seberang Yonif 202",
            "location_description": "Jl. Raya Tajur, seberang markas militer Yonif Mekanis 202/Tajimalela",
            "category": "PUBLIC",
            "latitude": -6.275124,
            "longitude": 106.994152,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Seberang_Yonif_202.m3u8",
        },
        {
            "camera_name": "Taman Kelurahan Jakasampura",
            "location_description": "Sektor rekreasi publik dan taman bermain Kelurahan Jakasampura",
            "category": "PUBLIC",
            "latitude": -6.248102,
            "longitude": 106.969452,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Taman_Kelurahan_Jakasampura.m3u8",
        },
        {
            "camera_name": "Universitas Bani Saleh",
            "location_description": "Jl. M. Hasibuan, halte bus depan gerbang masuk Universitas Bani Saleh",
            "category": "PUBLIC",
            "latitude": -6.245842,
            "longitude": 107.000154,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/Universitas_Bani_Saleh.m3u8",
        },
        {
            "camera_name": "Area Car Free Day Bekasi",
            "location_description": "Jl. Ahmad Yani, titik kumpul lintasan CFD Stadion Patriot Candrabhaga",
            "category": "PUBLIC",
            "latitude": -6.239124,
            "longitude": 106.993412,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/area_cfd.m3u8",
        },
        {
            "camera_name": "Bendungan Prisdo",
            "location_description": "Pintu air dan area pemantauan debit air Bendungan Prisdo Kali Malang",
            "category": "PUBLIC",
            "latitude": -6.246412,
            "longitude": 106.992154,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/bendungan_prisdo.m3u8",
        },
        {
            "camera_name": "Pertigaan Cevest",
            "location_description": "Jl. Guntur, persimpangan lampu lalu lintas di depan Balai Besar Cevest",
            "category": "PUBLIC",
            "latitude": -6.240154,
            "longitude": 106.995124,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/pertigaan_cevest.m3u8",
        },
        {
            "camera_name": "Proyek Bekasi",
            "location_description": "Kawasan pasar lama / pertokoan Proyek lama Bekasi Kota",
            "category": "PUBLIC",
            "latitude": -6.239451,
            "longitude": 107.006124,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/proyek_bekasi.m3u8",
        },
        {
            "camera_name": "Rawa Tembaga",
            "location_description": "Jalan Rawa Tembaga, area sekitar komplek perkantoran Pemkot Bekasi",
            "category": "PUBLIC",
            "latitude": -6.241154,
            "longitude": 106.991245,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/rawa_tembaga.m3u8",
        },
        {
            "camera_name": "Terminal Bekasi",
            "location_description": "Area pintu keluar jalur bus Antar Kota Dalam Provinsi (AKDP) Terminal Bekasi",
            "category": "PUBLIC",
            "latitude": -6.251412,
            "longitude": 107.017542,
            "source_url": "https://eofficev2.bekasikota.go.id/backupcctv/m3/terminal_bekasi.m3u8",
        }
    ]

    print("🌱 Mulai melakukan seeding CCTV Bekasi dengan koordinat...")
    
    current_time = datetime.now()
    

    hash_password = bcrypt.hashpw("123".encode("utf-8"),bcrypt.gensalt()).decode("utf-8")

    account = {
        "username" : "admin",
        "password" : hash_password,
    }

    account = await db.accounts.create(data=account)

    profile = {
        "account_id" : account.account_id,
        "fullname" : "Administrator",
        "number_phone" : "+62123456",
        "email" : "admin@gmail.com",\
        "role" : "OWNER"
    }

    await db.profile.create(data=profile)

    for cctv in bekasi_cctv:
        print(cctv)
        encrypted = encrypt_text(cctv["source_url"])

        print(encrypted)
        await db.ccvtv.create(
        data={
        "camera_name": cctv["camera_name"],
        "source_url": encrypted,
        "latitude": cctv["latitude"],
        "longitude": cctv["longitude"],
        "category": cctv["category"],
        "location_description": cctv["location_description"],
        "created_at": current_time
    }
)
        
    print("✅ Seeding selesai!")
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())