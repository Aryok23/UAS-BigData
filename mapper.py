#!/usr/bin/env python
import sys
import csv
import os

def mapper():
    filepath = os.environ.get("mapreduce_map_input_file", "Unknown.csv")
    filename = filepath.split("/")[-1]
    symbol = filename.split(".")[0]

    reader = csv.reader(sys.stdin)
    
    for row in reader:
        if len(row) < 6: continue
        if "Date" in row[1] or "Open" in row[2]: continue
        
        try:
            date = row[1] 
            open_price = float(row[2]) 
            high_price = float(row[3])
            low_price  = float(row[4])
            close_price = float(row[5]) 

            # Validasi Data
            if high_price == 0 or low_price == 0: continue
            if high_price < low_price: continue

            denominator = open_price
            if denominator == 0: denominator = close_price
            if denominator == 0: continue

            volatility = (high_price - low_price) / denominator
            volatility = abs(volatility)
            
            # Output: Symbol [TAB] Date [TAB] Close [TAB] Volatility
            print("{0}\t{1}\t{2}\t{3}".format(symbol, date, close_price, volatility))
            
        except ValueError:
            continue

if __name__ == "__main__":
    mapper()