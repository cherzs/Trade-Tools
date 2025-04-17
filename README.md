# Trade-Tools

Aplikasi web untuk membantu trader dalam mengelola risiko, mencatat transaksi, dan memproyeksikan keuntungan.

## Fitur Utama

1. **Risk & Position Size Calculator**
   - Menghitung ukuran posisi berdasarkan risiko
   - Menampilkan Risk-to-Reward Ratio

2. **Manual Trade Journal**
   - Mencatat histori transaksi trading
   - Menampilkan ringkasan performa (winrate, R:R rata-rata, total P/L)

3. **Expected Profit Projection**
   - Menghitung proyeksi keuntungan berdasarkan winrate dan R:R
   - Simulasi profit untuk jumlah trade tertentu

## Cara Menjalankan Aplikasi

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Jalankan aplikasi:
   ```
   streamlit run app/main.py
   ```

## Teknologi

- Streamlit untuk UI
- Pandas untuk manajemen data
- Plotly untuk visualisasi
