# Struktur Folder

uas-bigdata/

├── download_data.py

├── mapper.py

├── reducer.py

├── hasil_analisis/ (AUTO)

└── input_data/

# Pastikan docker sudah running

cek 
```
docker --version
```

kalo muncul hasil aman

# Masuk Root Docker dan buat container bernama "hadoop-saham"
```
docker run -it --user root --name hadoop-saham -v "${PWD}:/data" apache/hadoop:3 bash
```

# jalanin semua
```
/opt/hadoop/bin/hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
-input /data/input_data/ \
-output /data/hasil_analisis \
-mapper "python3 /data/mapper.py" \
-reducer "python3 /data/reducer.py"
```

# Kalo ga masuk docker bisa langsung command ini

```
docker exec hadoop-saham /opt/hadoop/bin/hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -input /data/input_data/ -output /data/hasil_analisis -mapper "python /data/mapper.py" -reducer "python /data/reducer.py"
```
