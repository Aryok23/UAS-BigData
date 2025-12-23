import kagglehub
import shutil
import os

print("Sedang mendownload data...")
# Download latest version
path = kagglehub.dataset_download("anukaggle81/usa-top-900-historic-dataset")

print("Data berhasil didownload di:", path)
print("Silakan buka file explorer di alamat tersebut, dan copy semua file .csv ke dalam folder uas-bigdata ini.")