import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- KONFIGURASI ---
# Pastikan path ini sesuai dengan folder output Hadoop terakhir kamu
# Bisa 'hasil_analisis/part-00000' atau 'hasil_tes/part-00000'
file_path = 'hasil_analisis/part-00000'

# Cek file
if not os.path.exists(file_path):
    print(f"Error: File {file_path} tidak ditemukan! Cek path folder.")
    exit()

print("Membaca data dari Hadoop...")

# 1. BACA DATA
df = pd.read_csv(file_path, sep='\t', names=['Symbol', 'Vol_Str', 'CAGR_Str', 'Label_Raw'])

# 2. BERSIHKAN DATA
df['Volatility'] = df['Vol_Str'].str.replace('%', '').astype(float)
df['CAGR'] = df['CAGR_Str'].str.replace('%', '').astype(float)

# Pisahkan Label
df[['Risk_Cat', 'Perf_Cat']] = df['Label_Raw'].str.split('|', expand=True)

# Set Style Grafik biar cantik
sns.set_style("whitegrid")

# =======================================================
# GAMBAR 1: SCATTER PLOT (RISK VS REWARD)
# =======================================================
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='Volatility', y='CAGR', hue='Risk_Cat', style='Perf_Cat', s=80, alpha=0.7)
plt.axhline(0, color='black', linewidth=1)
plt.axvline(3.0, color='red', linestyle='--')
plt.axvline(1.5, color='green', linestyle='--')

plt.title('RISK vs REWARD MATRIX (Analisis Saham USA)', fontsize=14)
plt.xlabel('Risiko (Volatilitas Harian %)')
plt.ylabel('Pertumbuhan Tahunan / CAGR (%)')

# Anotasi ekstrim
for i in range(df.shape[0]):
    if df.CAGR[i] > 60 or df.CAGR[i] < -60: # Ambang batas label teks
        plt.text(df.Volatility[i]+0.1, df.CAGR[i], df.Symbol[i], fontsize=8)

plt.tight_layout()
plt.savefig('grafik_1_kuadran.png')
print("Grafik 1 disimpan: grafik_1_kuadran.png")
plt.close()

# =======================================================
# GAMBAR 2: TOP 15 MONSTER GROWTH (Profit Tertinggi)
# =======================================================
top_growth = df.sort_values(by='CAGR', ascending=False).head(15)

plt.figure(figsize=(10, 6))
bars = plt.barh(top_growth['Symbol'], top_growth['CAGR'], color='mediumseagreen')
plt.xlabel('CAGR (%)')
plt.title('TOP 15 MONSTER GROWTH (Profit Tertinggi)', fontsize=14)
plt.gca().invert_yaxis()

for bar in bars:
    width = bar.get_width()
    plt.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('grafik_2_top_growth.png')
print("Grafik 2 disimpan: grafik_2_top_growth.png")
plt.close()

# =======================================================
# GAMBAR 3: TOP 15 PALING VOLATILE (GENERAL)
# "High Risk High Return" atau "High Risk Total Loss"? Campur semua.
# =======================================================
top_vol_all = df.sort_values(by='Volatility', ascending=False).head(15)

plt.figure(figsize=(10, 6))
# Pakai warna merah bata (salmon) untuk menandakan bahaya
bars = plt.barh(top_vol_all['Symbol'], top_vol_all['Volatility'], color='salmon')
plt.xlabel('Volatilitas Harian (%)')
plt.title('TOP 15 SAHAM PALING VOLATILE (Campur Profit & Rugi)', fontsize=14)
plt.gca().invert_yaxis()

for bar in bars:
    width = bar.get_width()
    # Tampilkan juga CAGR di sebelah bar volatilitas biar kelihatan konteksnya
    symbol_data = top_vol_all[top_vol_all['Volatility'] == width].iloc[0]
    cagr_val = symbol_data['CAGR']
    status = "(Untung)" if cagr_val >= 0 else "(Rugi)"
    
    label_text = f'{width:.2f}% Vol | CAGR: {cagr_val:.2f}% {status}'
    plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, label_text, va='center', fontsize=8)

plt.tight_layout()
plt.savefig('grafik_3_top_volatile_all.png')
print("Grafik 3 disimpan: grafik_3_top_volatile_all.png")
plt.close()

# =======================================================
# GAMBAR 4: TOP 15 VOLATILE (FILTER: NO LOSS)
# "Trader's Paradise": Bergerak liar, tapi tren jangka panjang positif
# =======================================================
# Filter: CAGR minimal 0 (Tidak Rugi)
df_no_loss = df[df['CAGR'] >= 0]
top_vol_safe = df_no_loss.sort_values(by='Volatility', ascending=False).head(15)

plt.figure(figsize=(10, 6))
# Pakai warna oranye/emas untuk "High Opportunity"
bars = plt.barh(top_vol_safe['Symbol'], top_vol_safe['Volatility'], color='orange')
plt.xlabel('Volatilitas Harian (%)')
plt.title('TOP 15 SAHAM VOLATILE TAPI TIDAK RUGI (CAGR >= 0%)', fontsize=14)
plt.gca().invert_yaxis()

for bar in bars:
    width = bar.get_width()
    symbol_data = top_vol_safe[top_vol_safe['Volatility'] == width].iloc[0]
    cagr_val = symbol_data['CAGR']
    
    label_text = f'{width:.2f}% Vol | CAGR: +{cagr_val:.2f}%'
    plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, label_text, va='center', fontsize=8)

plt.tight_layout()
plt.savefig('grafik_4_volatile_noloss.png')
print("Grafik 4 disimpan: grafik_4_volatile_noloss.png")
plt.show() # Tampilkan jendela popup terakhir