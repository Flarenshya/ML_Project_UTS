I. JUDUL PROYEK DAN DESKRIPSI SINGKAT

1. Judul Proyek          : SmartUploader — Sistem Otomatisasi Upload Video Berbasis AI 
2. Deskripsi Singkat     : 
SmartUploader adalah aplikasi berbasis Artificial Intelligence (AI) yang dirancang untuk mengotomatisasi proses upload video ke YouTube.
Melalui sistem ini, pengguna cukup mengisi beberapa informasi seperti judul, deskripsi, dan email, kemudian sistem akan secara otomatis:
- Mengunggah video ke YouTube melalui YouTube Data API v3.
- Melakukan analisis sentimen pada judul dan deskripsi video menggunakan model AI.
- Mengirimkan notifikasi hasil upload melalui n8n Automation Workflow (lewat email).


II. Daftar Anggota Kelompok (Nama & NIM).

1. Calvin Wijaya            - 22111
2. John Alexander Salim     - 221113056
3. Flarenshya Clearesta     - 221110278


III. Petunjuk Penggunaan Aplikasi (Cara menjalankan fungsi-fungsi utama).
1. Jalankan aplikasi melalui browser pada alamat http://localhost:5173
2. Pilih video yang ingin diunggah
3. Masukkan judul, deskripsi dan alamat email.
4. Klik tombol 'Upload'
Sistem akan secara otomatis:
- Mengirim data ke backend Flask
- Melakukan proses upload ke Youtube
- Melakukan analisis sentimen terhadap deskripsi YouTube
- Mengirim notifikasi hasil ke email melalui n8n workflow
5. Lihat hasil upload pada Channel YouTube
6. Notifikasi dikirim ke email sesuai pengaturan


IV. Petunjuk instalasi dan cara menjalankan proyek di lingkungan lokal.
1. Clone Repository
git clone https://github.com/Flarenshya/ML_Project_UTS
2. Instalasi Backend (Flask + AI Model)
python -m venv .venv
pip install -r requirements.txt
3. Jalankan backend
python -m backend.app
4. Instalasi Frontend (React + Vite)
cd frontend
npm install
5. Jalankan aplikasi
npm run dev
Frontend akan berjalan di http://localhost:5173
6. Jalankan n8n
n8n start

Akses aplikasi di browser, lalu lakukan uji upload video. 

lik onedrive: https://mikroskilacid-my.sharepoint.com/:f:/g/personal/221110278_students_mikroskil_ac_id/Ep0PWJmf2gtMvihNjCJ-QaABrUIFJ9fifW7kGsIG1R--5A?e=HC19yJ
