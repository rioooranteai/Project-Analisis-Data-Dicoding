# Dashboard Analisis Polusi Udara

*Proyek ini merupakan aplikasi Streamlit untuk menampilkan dan menganalisis data polusi udara di Distrik Changping.*

## Prasyarat

1. **Python 3.x**  
   Pastikan Python 3 sudah terinstall di komputer Anda.  
   Cek dengan:
   ```bash
   python --version
   ```
   atau
   ```bash
   python3 --version
   ```
2. **Git (opsional, jika Anda ingin melakukan clone repository dari GitHub)**  
   - Cek dengan `git --version`

## Langkah-Langkah Instalasi

### 1. Clone Repository (Opsional)

Jika Anda mengambil kode dari GitHub, gunakan:
```bash
git clone https://github.com/rioooranteai/Project-Analisis-Data-Dicoding.git
cd Project-Analisis-Data-Dicoding
```
Jika tidak menggunakan Git, pastikan Anda menempatkan seluruh file proyek (termasuk `dashboard.py`, `requirements.txt`, dan data CSV) di satu folder yang sama.

### 2. Membuat Virtual Environment

Sangat disarankan menggunakan *virtual environment* agar paket dan dependensi tidak berbenturan dengan proyek lain.

#### a) Menggunakan `venv` (bawaan Python)

```bash
# Di dalam folder proyek
python -m venv venv

# Aktifkan environment (Windows)
venv\Scripts\activate

# Aktifkan environment (macOS/Linux)
source venv/bin/activate
```

#### b) Menggunakan Anaconda/Miniconda (opsional)

```bash
conda create -n changping_dashboard python=3.9
conda activate changping_dashboard
```

### 3. Instalasi Requirements

Pastikan Anda sudah berada di dalam *virtual environment*. Lalu jalankan:

```bash
pip install -r requirements.txt
```

**Catatan**: Jika Anda menggunakan `conda`, Anda juga dapat memasang *library* secara manual atau menggunakan `pip install` di dalam environment Conda.

### 4. Menjalankan Dashboard

Setelah instalasi berhasil, Anda dapat menjalankan *dashboard* dengan perintah:

```bash
streamlit run dashboard.py
```

Perintah ini akan memulai *server* lokal Streamlit dan membuka tab baru di peramban (biasanya di http://localhost:8501).

