# =========================================================
# PROJECT AKHIR PENGOLAHAN CITRA DIGITAL
# IMPLEMENTASI EDGE DETECTION MULTI DATASET
#
# Metode:
# 1. Sobel
# 2. Prewitt
# 3. Canny
#
# Evaluasi:
# - MSE
# - PSNR
#
# Dataset:
# - Wajah
# - Plat Nomor
# - Dedaunan
# - Aerial/Satelit
#
# Mendukung MULTIPLE IMAGE tiap kategori
# =========================================================

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from math import log10, sqrt

# =========================================================
# STRUKTUR FOLDER DATASET
# =========================================================
#
# dataset/
# ├── wajah/
# │   ├── wajah1.jpg
# │   ├── wajah2.jpg
# │   └── wajah3.jpg
# │
# ├── plat_nomor/
# │   ├── plat1.jpg
# │   ├── plat2.jpg
# │   └── plat3.jpg
# │
# ├── dedaunan/
# │   ├── daun1.jpg
# │   ├── daun2.jpg
# │   └── daun3.jpg
# │
# ├── aerial/
# │   ├── aerial1.jpg
# │   ├── aerial2.jpg
# │   └── aerial3.jpg
#
# =========================================================

DATASET_FOLDERS = {
    "wajah": "dataset/wajah",
    "plat_nomor": "dataset/plat_nomor",
    "dedaunan": "dataset/dedaunan",
    "aerial": "dataset/aerial"
}

OUTPUT_FOLDER = "output"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# =========================================================
# PREPROCESSING
# =========================================================

def preprocessing(image):

    # Resize
    image = cv2.resize(image, (512, 512))

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    return gray, blur


# =========================================================
# SOBEL
# =========================================================

def sobel_detection(image):

    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    sobel = np.sqrt(sobel_x**2 + sobel_y**2)

    sobel = np.uint8(np.absolute(sobel))

    return sobel


# =========================================================
# PREWITT
# =========================================================

def prewitt_detection(image):

    kernel_x = np.array([
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ])

    kernel_y = np.array([
        [-1, -1, -1],
        [0, 0, 0],
        [1, 1, 1]
    ])

    prewitt_x = cv2.filter2D(image, -1, kernel_x)
    prewitt_y = cv2.filter2D(image, -1, kernel_y)

    prewitt = prewitt_x + prewitt_y

    return prewitt


# =========================================================
# CANNY
# =========================================================

def canny_detection(image):

    canny = cv2.Canny(image, 100, 200)

    return canny


# =========================================================
# MSE
# =========================================================

def calculate_mse(original, processed):

    mse = np.mean((original - processed) ** 2)

    return mse


# =========================================================
# PSNR
# =========================================================

def calculate_psnr(original, processed):

    mse = calculate_mse(original, processed)

    if mse == 0:
        return 100

    max_pixel = 255.0

    psnr = 20 * log10(max_pixel / sqrt(mse))

    return psnr


# =========================================================
# SIMPAN GAMBAR
# =========================================================

def save_image(folder_name, filename, image):

    folder_path = os.path.join(OUTPUT_FOLDER, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    output_path = os.path.join(folder_path, filename)

    cv2.imwrite(output_path, image)


# =========================================================
# VISUALISASI
# =========================================================

def display_results(title, original, sobel, prewitt, canny):

    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.title("Original")
    plt.axis("off")

    plt.subplot(2, 2, 2)
    plt.imshow(sobel, cmap='gray')
    plt.title("Sobel")
    plt.axis("off")

    plt.subplot(2, 2, 3)
    plt.imshow(prewitt, cmap='gray')
    plt.title("Prewitt")
    plt.axis("off")

    plt.subplot(2, 2, 4)
    plt.imshow(canny, cmap='gray')
    plt.title("Canny")
    plt.axis("off")

    plt.suptitle(title)

    plt.tight_layout()

    plt.show()


# =========================================================
# PROSES SATU GAMBAR
# =========================================================

def process_image(category_name, image_name, image_path):

    print("=" * 70)
    print(f"Kategori : {category_name}")
    print(f"Gambar   : {image_name}")
    print("=" * 70)

    image = cv2.imread(image_path)

    if image is None:
        print(f"Gagal membaca gambar : {image_path}")
        return

    # =====================================================
    # PREPROCESSING
    # =====================================================

    gray, blur = preprocessing(image)

    # =====================================================
    # EDGE DETECTION
    # =====================================================

    sobel_result = sobel_detection(blur)
    prewitt_result = prewitt_detection(blur)
    canny_result = canny_detection(blur)

    # =====================================================
    # EVALUASI MSE
    # =====================================================

    mse_sobel = calculate_mse(gray, sobel_result)
    mse_prewitt = calculate_mse(gray, prewitt_result)
    mse_canny = calculate_mse(gray, canny_result)

    # =====================================================
    # EVALUASI PSNR
    # =====================================================

    psnr_sobel = calculate_psnr(gray, sobel_result)
    psnr_prewitt = calculate_psnr(gray, prewitt_result)
    psnr_canny = calculate_psnr(gray, canny_result)

    # =====================================================
    # PRINT HASIL
    # =====================================================

    print("\nHASIL EVALUASI")

    print("\nSOBEL")
    print(f"MSE  : {mse_sobel:.2f}")
    print(f"PSNR : {psnr_sobel:.2f}")

    print("\nPREWITT")
    print(f"MSE  : {mse_prewitt:.2f}")
    print(f"PSNR : {psnr_prewitt:.2f}")

    print("\nCANNY")
    print(f"MSE  : {mse_canny:.2f}")
    print(f"PSNR : {psnr_canny:.2f}")

    # =====================================================
    # SIMPAN HASIL
    # =====================================================

    base_name = os.path.splitext(image_name)[0]

    # Preprocessing Result
    save_image(category_name, f"{base_name}_grayscale.jpg", gray)
    save_image(category_name, f"{base_name}_gaussian_blur.jpg", blur)

    # Edge Detection Result
    save_image(category_name, f"{base_name}_sobel.jpg", sobel_result)
    save_image(category_name, f"{base_name}_prewitt.jpg", prewitt_result)
    save_image(category_name, f"{base_name}_canny.jpg", canny_result)

    # =====================================================
    # VISUALISASI
    # =====================================================

    # display_results(
    #     f"{category_name} - {image_name}",
    #     gray,
    #     sobel_result,
    #     prewitt_result,
    #     canny_result
    # )


# =========================================================
# PROSES SEMUA DATASET DALAM SATU KATEGORI
# =========================================================

def process_category(category_name, folder_path):

    print("\n")
    print("#" * 70)
    print(f"MEMPROSES KATEGORI : {category_name}")
    print("#" * 70)

    if not os.path.exists(folder_path):
        print(f"Folder tidak ditemukan : {folder_path}")
        return

    image_files = os.listdir(folder_path)

    supported_extensions = ('.jpg', '.jpeg', '.png')

    image_files = [
        file for file in image_files
        if file.lower().endswith(supported_extensions)
    ]

    if len(image_files) == 0:
        print("Tidak ada gambar dalam folder.")
        return

    for image_name in image_files:

        image_path = os.path.join(folder_path, image_name)

        process_image(category_name, image_name, image_path)


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    print("\n")
    print("=" * 70)
    print("PROJECT AKHIR PENGOLAHAN CITRA DIGITAL")
    print("IMPLEMENTASI MULTI DATASET EDGE DETECTION")
    print("=" * 70)

    for category_name, folder_path in DATASET_FOLDERS.items():

        process_category(category_name, folder_path)

    print("\nSEMUA DATASET TELAH DIPROSES")
    print(f"Hasil tersimpan pada folder : {OUTPUT_FOLDER}")


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()