#!/usr/bin/env python
import sys
from datetime import datetime

def reducer():
    current_symbol = None
    
    total_volatility = 0
    count = 0
    
    # Kita butuh format tanggal untuk hitung selisih hari
    # Format di CSV kamu: YYYY-MM-DD (2020-12-10)
    date_fmt = '%Y-%m-%d'
    
    min_date_obj = None
    max_date_obj = None
    start_price = 0
    end_price = 0
    
    for line in sys.stdin:
        line = line.strip()
        parts = line.split("\t")
        
        if len(parts) != 4: continue
        
        symbol, date_str, close, vol = parts
        
        try:
            close = float(close)
            vol = float(vol)
            current_date = datetime.strptime(date_str, date_fmt)
        except ValueError:
            continue
            
        if current_symbol == symbol:
            total_volatility += vol
            count += 1
            
            # Cek Tanggal Awal
            if min_date_obj is None or current_date < min_date_obj:
                min_date_obj = current_date
                start_price = close
            
            # Cek Tanggal Akhir
            if max_date_obj is None or current_date > max_date_obj:
                max_date_obj = current_date
                end_price = close
                
        else:
            if current_symbol:
                process_result(current_symbol, total_volatility, count, start_price, end_price, min_date_obj, max_date_obj)
            
            # Reset
            current_symbol = symbol
            total_volatility = vol
            count = 1
            min_date_obj = current_date
            max_date_obj = current_date
            start_price = close
            end_price = close
            
    if current_symbol:
        process_result(current_symbol, total_volatility, count, start_price, end_price, min_date_obj, max_date_obj)

def process_result(symbol, total_volatility, count, start_price, end_price, min_date, max_date):
    # 1. Rata-rata Volatilitas Harian
    avg_vol = (total_volatility / count) * 100
    
    # 2. Hitung Durasi Tahun (CAGR Logic)
    if min_date and max_date and start_price > 0:
        days_diff = (max_date - min_date).days
        years = days_diff / 365.25
        
        cagr = 0
        if years < 1:
            # Jika data kurang dari 1 tahun, jangan pakai pangkat (bisa bias/error)
            # Pakai simple return saja
            cagr = ((end_price - start_price) / start_price) * 100
        else:
            # Rumus CAGR: (End/Start)^(1/Tahun) - 1
            # Kita pakai try-except takut ada math error (misal akar negatif meski jarang di saham)
            try:
                cagr = ((end_price / start_price) ** (1.0 / years) - 1) * 100
            except:
                cagr = 0
    else:
        cagr = 0
    
    # 3. Labeling Insight
    # Kriteria Growth Tahunan (CAGR):
    # > 20% per tahun = MONSTER GROWTH
    # 10-20% per tahun = HEALTHY
    # 0-10% per tahun = SLOW
    # < 0% = LOSING MONEY
    
    perform_label = "SLOW"
    if cagr > 20: perform_label = "MONSTER_GROWTH"
    elif cagr > 10: perform_label = "HEALTHY"
    elif cagr < 0: perform_label = "LOSS"
    
    risk_label = "Medium"
    if avg_vol < 1.5: risk_label = "Low_Risk"
    elif avg_vol > 3.0: risk_label = "High_Risk"
    
    # Output: Symbol [TAB] Volatility [TAB] CAGR(PerTahun) [TAB] Label
    print("{0}\t{1:.4f}%\t{2:.2f}%\t{3}|{4}".format(symbol, avg_vol, cagr, risk_label, perform_label))

if __name__ == "__main__":
    reducer()