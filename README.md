# DIP Final Project - Image Processing

Deskripsi singkat: repository ini berisi skrip pemrosesan citra untuk beberapa kategori dataset (aerial, dedaunan, plat_nomor, wajah). File utama untuk menjalankan pipeline adalah `main.py`.

## Prasyarat
- Python 3.8+ terinstall
- Virtual environment (opsional tapi direkomendasikan)

## Instalasi
1. Buka terminal di folder proyek (root repository).
2. Buat dan aktifkan virtual environment:

Windows (PowerShell/CMD):
```powershell
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependency:
```bash
pip install -r requirements.txt
```

## Struktur dataset
Letakkan dataset di folder `dataset/` dengan struktur sebagai berikut (sudah ada contoh dalam repositori):

- `dataset/aerial/`
- `dataset/dedaunan/`
- `dataset/plat_nomor/`
- `dataset/wajah/`

Output hasil pemrosesan akan disimpan di folder `output/` dengan subfolder yang sesuai (aerial, dedaunan, plat_nomor, wajah).

## Menjalankan proyek
Jalankan file utama dari root proyek:

```bash
python main.py
```

Jika `main.py` menerima argumen atau konfigurasi tambahan, silakan lihat komentar di bagian atas file `main.py` atau hubungi pengembang.

## Troubleshooting singkat
- Jika muncul error paket tidak ditemukan, pastikan virtualenv aktif dan `pip install -r requirements.txt` dijalankan.
- Pada Windows, gunakan `venv\Scripts\activate` di PowerShell/CMD.

## Kontak
Jika butuh bantuan tambahan, berikan pesan error atau jelaskan langkah yang sudah dicoba.
