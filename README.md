# UAS Big Data: Historic Stock Analysis with Hadoop MapReduce 📈

Repository ini berisi implementasi tugas akhir mata kuliah **Big Data dan Analitik** untuk menganalisis risiko (Volatilitas) dan keuntungan (CAGR) dari 959+ saham Amerika Serikat menggunakan **Hadoop MapReduce**.

## 🚀 Fitur Utama
* **Big Data Processing**: Mengolah ribuan file CSV secara paralel menggunakan Hadoop Streaming.
* **Risk Analysis**: Menghitung volatilitas harian rata-rata.
* **Growth Analysis**: Menghitung Compound Annual Growth Rate (CAGR) untuk data time-series.
* **Visualization**: Menghasilkan matriks Risk vs Reward dan grafik kinerja saham.

## 📂 Struktur Folder

```
uas-bigdata/
├── input_data/         # (Wajib) Letakkan file CSV saham di sini
├── hasil_analisis/     # (Auto) Output hasil perhitungan Hadoop
├── download_data.py    # Script untuk mengunduh dataset (Opsional)
├── mapper.py           # Logika Mapping (Data Cleaning & Volatility Calc)
├── reducer.py          # Logika Reducing (Aggregation & CAGR Calc)
├── visual_grafik.py    # Script Python untuk generate chart dari hasil analisis
└── README.md           # Dokumentasi proyek
```

🛠️ **Prasyarat**
Pastikan perangkat Anda sudah terinstal:

* **Docker Desktop** (Running)
* **Python 3.x** (Di Host/Laptop, untuk visualisasi)
* **Pandas, Matplotlib, Seaborn** (pip install pandas matplotlib seaborn)

## ⚡ **Cara Menjalankan (Quick Start)**

**1. Persiapan Container**

Pastikan Docker sudah berjalan. Cek dengan:

```
docker --version
```
Jalankan perintah berikut untuk membuat container Hadoop dan melakukan mounting folder kerja saat ini ke dalam Docker: (Jalankan di terminal VS Code / PowerShell)

```
docker run -d -it --name hadoop-saham -v "${PWD}:/data" apache/hadoop:3 bash
```

**Catatan**: Jika container sudah pernah dibuat, cukup jalankan `docker start hadoop-saham`.

**2. Jalankan MapReduce**

Sebelum menjalankan job baru, pastikan folder output lama dihapus agar Hadoop tidak error.

**Langkah 1: Hapus Output Lama**
```
docker exec hadoop-saham rm -rf /data/hasil_analisis
```

**Langkah 2: Eksekusi Hadoop Streaming** Perintah ini akan menjalankan MapReduce menggunakan Python 2.7 bawaan container:

```
docker exec hadoop-saham /opt/hadoop/bin/hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
-input /data/input_data/ \
-output /data/hasil_analisis \
-mapper "python /data/mapper.py" \
-reducer "python /data/reducer.py"
```

**3. Cek Hasil**

Jika sukses, hasil analisis akan muncul di folder lokal `hasil_analisis/part-00000`.

**4. Visualisasi Data**

Untuk membuat grafik (Scatter Plot Kuadran, Bar Chart Top Growth, dll), jalankan script visualisasi di laptop lokal Anda:

```
python visual_grafik.py
```
Grafik PNG akan otomatis tergenerate di folder root.

## 📝 Catatan Teknis
* **Environment**: Menggunakan `apache/hadoop:3` (CentOS basis).
* **Python Runtime**:
  * _Docker Side_: Python 2.7.5 (untuk Mapper/Reducer).
  * _Host Side_: Python 3.x (untuk Visualisasi).
* **Data Handling**: Input data dibaca menggunakan _Local File System abstraction_ (`file:///`) melalui Docker Volume mounting untuk efisiensi I/O.
