# Sistem PPDB Online SMA Negeri 1 Bandung

Sistem Penerimaan Peserta Didik Baru (PPDB) Online untuk SMA Negeri 1 Bandung dengan fitur pendaftaran, verifikasi, dan pembayaran.

## Fitur Utama

### Calon Siswa
1. Pendaftaran Akun
   - Registrasi username dan password
   - Login sistem
   - Dashboard siswa

2. Form Pendaftaran
   - Input data pribadi (nama, tempat lahir, jenis kelamin, agama, dll)
   - Input data orang tua (nama dan pekerjaan orang tua)
   - Pilihan jurusan (IPA/IPS)
   - Upload dokumen (ijazah dan foto)
   - Progress tracking pendaftaran

3. Status Pendaftaran
   - Tracking progress (Pendaftaran -> Verifikasi -> Pembayaran)
   - Notifikasi status pendaftaran
   - Status verifikasi admin

4. Pembayaran
   - Informasi rekening pembayaran
   - Upload bukti transfer
   - Status verifikasi pembayaran

### Admin
1. Dashboard Admin
   - Statistik pendaftaran
   - Data pendaftar
   - Manajemen user

2. Verifikasi Pendaftaran
   - Review data pendaftar
   - Verifikasi dokumen
   - Approval/Reject pendaftaran

3. Manajemen Jadwal
   - Input jadwal pelajaran
   - Edit jadwal
   - Hapus jadwal

4. Manajemen Pembayaran
   - Verifikasi bukti pembayaran
   - Update status pembayaran
   - Laporan pembayaran

## Teknologi

- Backend: Python Flask
- Database: SQLite
- Frontend: 
  - Bootstrap 4
  - jQuery
  - Font Awesome icons
- File Upload: Werkzeug

## Struktur Database

### Tabel User
- id (Primary Key)
- username
- password
- role (admin/user)
- status (pending/accepted/rejected)
- full_name
- gender
- agama
- phone
- address
- jurusan
- tempat_lahir
- asal_sekolah
- nama_ayah
- pekerjaan_ayah
- nama_ibu
- pekerjaan_ibu
- payment_status
- payment_proof

### Tabel Schedule
- id (Primary Key)
- jurusan
- waktu
- senin
- selasa
- rabu
- kamis
- jumat

## Instalasi

1. Clone repository
```bash
git clone [url-repository]
cd calya
```

2. Buat virtual environment
```bash
python -m venv venv
source venv/bin/activate  
venv\Scripts\activate    
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Siapkan database
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Jalankan aplikasi
```bash
python app.py
```

## Penggunaan

### Login Admin
- Username: admin
- Password: admin123
- URL: /admin_login

### Register Siswa
1. Klik "Register" di halaman utama
2. Isi username dan password
3. Login dengan akun yang dibuat
4. Lengkapi form pendaftaran
5. Upload dokumen yang diperlukan
6. Tunggu verifikasi admin

### Alur Sistem
1. Siswa mendaftar akun
2. Siswa melengkapi data diri
3. Admin melakukan verifikasi
4. Jika diterima, siswa melakukan pembayaran
5. Admin verifikasi pembayaran
6. Proses selesai

## Kontribusi
1. Fork repository
2. Buat branch baru
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## Lisensi
MIT License

## Screenshots

### Home Page & Informasi Awal
<img src="static/sss/home page.png" alt="Homepage" width="800"/>
Halaman utama website PPDB yang menampilkan menu navigasi dan informasi pendaftaran.

<img src="static/sss/langkah pendaftaran.png" alt="Registration Steps" width="800"/>
Panduan langkah-langkah proses pendaftaran PPDB secara detail.

<img src="static/sss/kualitas.png" alt="School Quality" width="800"/>
Informasi tentang kualitas dan prestasi sekolah.

### Registrasi & Login
<img src="static/sss/register.png" alt="Registration Form" width="800"/>
Form registrasi akun baru untuk calon siswa.

<img src="static/sss/login.png" alt="Login Page" width="800"/>
Halaman login untuk siswa.

<img src="static/sss/login admin.png" alt="Admin Login" width="800"/>
Halaman login khusus admin.

### Proses Pendaftaran
<img src="static/sss/setelah daftar.png" alt="Post Registration" width="800"/>
Tampilan setelah siswa berhasil mendaftar.

<img src="static/sss/verifikasi siswa data pribadi.png" alt="Personal Data Verification" width="800"/>
Form pengisian data pribadi calon siswa.

<img src="static/sss/tulisan jika siswa diterima.png" alt="Acceptance Notice" width="800"/>
Notifikasi penerimaan siswa.

<img src="static/sss/jika ditolak.png" alt="Rejection Notice" width="800"/>
Notifikasi yang muncul ketika pendaftaran siswa ditolak oleh admin setelah proses verifikasi.

### Pembayaran
<img src="static/sss/jika diterima muncul halaman pembayaran.png" alt="Payment Page" width="800"/>
Halaman pembayaran setelah siswa diterima.

<img src="static/sss/pengisian pembayaran.png" alt="Payment Form" width="800"/>
Form pengisian data pembayaran.

<img src="static/sss/pembayaran.png" alt="Payment Details" width="800"/>
Detail informasi pembayaran.

<img src="static/sss/submit pembayaran.png" alt="Payment Submission" width="800"/>
Konfirmasi pengiriman bukti pembayaran.

<img src="static/sss/status pembayaran.png" alt="Payment Status" width="800"/>
Status verifikasi pembayaran.

### Panel Admin
<img src="static/sss/dashboard admin.png" alt="Admin Dashboard" width="800"/>
Dashboard utama admin.

<img src="static/sss/tampilan data di admin.png" alt="Admin Data View 1" width="800"/>
Tampilan data pendaftar di panel admin.

<img src="static/sss/tampilan data diadmin 2.png" alt="Admin Data View 2" width="800"/>
Detail data pendaftar yang dapat dikelola admin.

<img src="static/sss/tampilan data di admin 3.png" alt="Admin Data View 3" width="800"/>
Manajemen status pendaftaran siswa.

<img src="static/sss/bukti pembayaran muncul di admin.png" alt="Payment Verification Admin" width="800"/>
Panel verifikasi bukti pembayaran oleh admin.

<img src="static/sss/pembayaran masuk ke laporan.png" alt="Payment Reports" width="800"/>
Laporan pembayaran yang telah masuk.

<img src="static/sss/laporan.png" alt="Reports" width="800"/>
Halaman laporan keseluruhan sistem.

### Manajemen Jadwal
<img src="static/sss/kelola jadwal pelajaran.png" alt="Schedule Management" width="800"/>
Halaman pengelolaan jadwal pelajaran.

<img src="static/sss/menambah jadwal baru.png" alt="Add New Schedule" width="800"/>
Form penambahan jadwal baru.

<img src="static/sss/edit jadwal.png" alt="Edit Schedule" width="800"/>
Form edit jadwal pelajaran.

<img src="static/sss/jadwal.png" alt="Schedule View" width="800"/>
Tampilan jadwal pelajaran.

<img src="static/sss/selesai.png" alt="Completion Page" width="800"/>
Halaman konfirmasi yang menunjukkan bahwa seluruh proses pendaftaran telah selesai dan berhasil dilakukan.
