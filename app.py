from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import mysql.connector
from fpdf import FPDF
import os
from datetime import date

app = Flask(__name__)
app.secret_key = 'Alif123'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_raport_m_alif'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    nis = request.args.get('nis', '').strip()
    mapel = request.args.get('mapel', '').strip()
    semester = request.args.get('semester', '').strip()
    tahun = request.args.get('tahun', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        a.id_nilai,
        a.nis,
        c.Nama,
        b.nama_mapel,
        a.nilai_tugas,
        a.nilai_uts,
        a.nilai_uas,
        a.nilai_akhir,
        a.Deskripsi,
        a.Semester,
        a.tahun_ajaran
    FROM nilai_alif a
    JOIN mapel_alif b ON a.id_mapel = b.id_mapel
    JOIN siswa_alif c ON a.nis = c.nis
    WHERE 1=1
    """
    params = []

    if nis:
        query += " AND (a.nis LIKE %s OR c.Nama LIKE %s)"
        params.extend([f'%{nis}%', f'%{nis}%'])
    
    if mapel:
        query += " AND b.nama_mapel=%s"
        params.append(mapel)
    
    if semester:
        query += " AND a.Semester=%s"
        params.append(semester)
    
    if tahun:
        query += " AND a.tahun_ajaran=%s"
        params.append(tahun)

    cursor.execute(query, params)
    siswa = cursor.fetchall()

    cursor.execute("SELECT DISTINCT nama_mapel FROM mapel_alif ORDER BY nama_mapel")
    mapel_list = [row['nama_mapel'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT tahun_ajaran FROM nilai_alif ORDER BY tahun_ajaran DESC")
    tahun_list = [row['tahun_ajaran'] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return render_template(
        'index.html',
        siswa=siswa,
        mapel_list=mapel_list,
        tahun_list=tahun_list
    )

@app.route('/hapus_nilai/<nis>/<mapel>/<semester>/<tahun>')
def hapus_nilai_alif(nis, mapel, semester, tahun):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE a FROM nilai_alif a
        JOIN mapel_alif b ON a.id_mapel=b.id_mapel
        WHERE a.nis=%s AND b.nama_mapel=%s
        AND a.Semester=%s AND a.tahun_ajaran=%s
    """, (nis, mapel, semester, tahun))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Data nilai berhasil dihapus!', 'success')
    return redirect(url_for('index'))

@app.route('/edit_nilai/<nis>/<mapel>/<semester>/<tahun>')
def edit_nilai_alif(nis, mapel, semester, tahun):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.nis,c.Nama,b.nama_mapel,
               a.nilai_tugas,a.nilai_uts,a.nilai_uas,
               a.Deskripsi,a.Semester,a.tahun_ajaran
        FROM nilai_alif a
        JOIN mapel_alif b ON a.id_mapel=b.id_mapel
        JOIN siswa_alif c ON a.nis=c.nis
        WHERE a.nis=%s AND b.nama_mapel=%s
        AND a.Semester=%s AND a.tahun_ajaran=%s
    """, (nis, mapel, semester, tahun))

    data = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('edit_nilai.html', data=data)

@app.route('/update_nilai', methods=['POST'])
def update_nilai_alif():
    nis = request.form['nis']
    mapel = request.form['mapel']
    semester = request.form['semester']
    tahun = request.form['tahun']
    tugas = request.form['nilai_tugas']
    uts = request.form['nilai_uts']
    uas = request.form['nilai_uas']
    deskripsi = request.form['deskripsi']

    nilai_akhir = (int(tugas) + int(uts) + int(uas)) / 3

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE nilai_alif a
        JOIN mapel_alif b ON a.id_mapel=b.id_mapel
        SET a.nilai_tugas=%s,a.nilai_uts=%s,a.nilai_uas=%s,
            a.nilai_akhir=%s,a.Deskripsi=%s
        WHERE a.nis=%s AND b.nama_mapel=%s
        AND a.Semester=%s AND a.tahun_ajaran=%s
    """, (tugas, uts, uas, nilai_akhir, deskripsi, nis, mapel, semester, tahun))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Data nilai berhasil diperbarui!', 'success')
    return redirect(url_for('index'))

@app.route('/tambah_nilai')
def tambah_nilai_alif():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT nis,Nama FROM siswa_alif")
    siswa = cursor.fetchall()

    cursor.execute("SELECT id_mapel,nama_mapel FROM mapel_alif")
    mapel = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('tambah_nilai.html', siswa=siswa, mapel=mapel)

@app.route('/simpan_nilai', methods=['POST'])
def simpan_nilai_alif():
    nis = request.form['nis']
    id_mapel = request.form['id_mapel']
    semester = request.form['Semester']
    tahun = request.form['tahun']
    tugas = request.form['nilai_tugas']
    uts = request.form['nilai_uts']
    uas = request.form['nilai_uas']
    deskripsi = request.form['deskripsi']

    nilai_akhir = (int(tugas) + int(uts) + int(uas)) / 3

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_nilai FROM nilai_alif
        WHERE id_nilai LIKE 'NP%'
        ORDER BY id_nilai DESC LIMIT 1
    """)
    last = cursor.fetchone()

    if last:
        nomor = int(last[0][2:]) + 1
        id_baru = f"NP{nomor:03d}"
    else:
        id_baru = "NP001"

    cursor.execute("""
        INSERT INTO nilai_alif
        (id_nilai,nis,id_mapel,nilai_tugas,nilai_uts,nilai_uas,
         nilai_akhir,Deskripsi,Semester,tahun_ajaran)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (id_baru, nis, id_mapel, tugas, uts, uas,
          nilai_akhir, deskripsi, semester, tahun))

    conn.commit()
    cursor.close()
    conn.close()

    flash(f'Data nilai berhasil ditambahkan ({id_baru})', 'success')
    return redirect(url_for('index'))

@app.route('/cetak_pdf/<nis>/<semester>/<tahun>')
def cetak_pdf(nis, semester, tahun):

    def row_height(pdf, text, width, line_height):
        text = str(text)
        if not text:
            return line_height
        nb_lines = pdf.get_string_width(text) / width
        return max(line_height, (int(nb_lines) + 1) * line_height)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.Nama, c.tgl_lahir, k.nama_kelas AS kelas, a.nis, b.nama_mapel,
               a.nilai_tugas, a.nilai_uts, a.nilai_uas,
               a.nilai_akhir, a.Deskripsi
        FROM nilai_alif a
        JOIN mapel_alif b ON a.id_mapel=b.id_mapel
        JOIN siswa_alif c ON a.nis=c.nis
        JOIN kelas_alif k ON c.id_kelas=k.id_kelas
        WHERE a.nis=%s AND a.Semester=%s AND a.tahun_ajaran=%s
    """, (nis, semester, tahun))

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    pdf_folder = "raport_siswa"
    os.makedirs(pdf_folder, exist_ok=True) 

    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)

    pdf.set_font('DejaVu', '', 14)
    pdf.cell(0, 8, 'LAPORAN HASIL BELAJAR', ln=True, align='C')
    pdf.set_font('DejaVu', '', 11)
    pdf.cell(0, 6, 'SMK Negeri 2 Cimahi', ln=True, align='C')
    pdf.set_font('DejaVu', '', 8)
    pdf.cell(0, 4, ' Jl. Kamarung KM. 1,5 No. 69, Kelurahan Citeureup, Kecamatan Cimahi Utara, Kota Cimahi, Jawa Barat', ln=True, align='C')
    pdf.ln(6)

    if data:
        tgl_lahir = data[0]["tgl_lahir"]
        kelas = data[0]["kelas"]
        pdf.cell(40, 6, 'NIS', 0)
        pdf.cell(0, 6, f': {nis}', ln=True)
        pdf.cell(40, 6, 'Nama', 0)
        pdf.cell(0, 6, f': {data[0]["Nama"]}', ln=True)
        pdf.cell(40, 6, 'Tanggal Lahir', 0)
        pdf.cell(0, 6, f': {tgl_lahir}', ln=True)
        pdf.cell(40, 6, 'Kelas', 0)
        pdf.cell(0, 6, f': {kelas}', ln=True)  
        pdf.cell(40, 6, 'Semester', 0)
        pdf.cell(0, 6, f': {semester}', ln=True)
        pdf.cell(40, 6, 'Tahun Ajaran', 0)
        pdf.cell(0, 6, f': {tahun}', ln=True)

    pdf.ln(6)

    pdf.set_font('DejaVu', '', 10)
    pdf.cell(10, 8, 'No', 1, 0, 'C')
    pdf.cell(50, 8, 'Mata Pelajaran', 1, 0, 'C')
    pdf.cell(20, 8, 'Tugas', 1, 0, 'C')
    pdf.cell(20, 8, 'UTS', 1, 0, 'C')
    pdf.cell(20, 8, 'UAS', 1, 0, 'C')
    pdf.cell(25, 8, 'Nilai Akhir', 1, 0, 'C')
    pdf.cell(45, 8, 'Deskripsi', 1, 1, 'C')

    no = 1
    for d in data:
        line_height = 8
        row_h = row_height(pdf, d['Deskripsi'], 45, line_height)

        if pdf.get_y() + row_h > 270:
            pdf.add_page()
            pdf.set_font('DejaVu', '', 10)
            pdf.cell(10, 8, 'No', 1, 0, 'C')
            pdf.cell(50, 8, 'Mata Pelajaran', 1, 0, 'C')
            pdf.cell(20, 8, 'Tugas', 1, 0, 'C')
            pdf.cell(20, 8, 'UTS', 1, 0, 'C')
            pdf.cell(20, 8, 'UAS', 1, 0, 'C')
            pdf.cell(25, 8, 'Nilai Akhir', 1, 0, 'C')
            pdf.cell(45, 8, 'Deskripsi', 1, 1, 'C')

        x = pdf.get_x()
        y = pdf.get_y()

        pdf.cell(10, row_h, str(no), 1, 0, 'C')
        pdf.cell(50, row_h, d['nama_mapel'], 1, 0)
        pdf.cell(20, row_h, str(d['nilai_tugas']), 1, 0, 'C')
        pdf.cell(20, row_h, str(d['nilai_uts']), 1, 0, 'C')
        pdf.cell(20, row_h, str(d['nilai_uas']), 1, 0, 'C')
        pdf.cell(25, row_h, str(d['nilai_akhir']), 1, 0, 'C')

        pdf.set_xy(x + 145, y)
        pdf.multi_cell(45, line_height, d['Deskripsi'], 1)

        pdf.set_xy(x, y + row_h)
        no += 1

    pdf.ln(15)
    pdf.cell(0, 6, 'Mengetahui,', ln=True)

    pdf.ln(15)
    pdf.cell(90, 6, 'Wali Kelas', 0, 0, 'C')
    pdf.cell(0, 6, 'Kepala Sekolah', 0, 1, 'C')

    pdf.ln(20)
    pdf.cell(90, 6, '(............................)', 0, 0, 'C')
    pdf.cell(0, 6, '(............................)', 0, 1, 'C')

    filename = os.path.join(pdf_folder, f"laporan_{nis}.pdf")
    pdf.output(filename)

    return send_file(filename, as_attachment=True)


@app.route('/cetak_semua_pdf')
def cetak_semua_pdf():
    nis = request.args.get('nis', '').strip()
    mapel = request.args.get('mapel', '').strip()
    semester = request.args.get('semester', '').strip()
    tahun = request.args.get('tahun', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT DISTINCT a.nis, a.Semester, a.tahun_ajaran, c.Nama, k.nama_kelas
    FROM nilai_alif a
    JOIN mapel_alif b ON a.id_mapel = b.id_mapel
    JOIN siswa_alif c ON a.nis = c.nis
    JOIN kelas_alif k ON c.id_kelas = k.id_kelas
    WHERE 1=1
    """
    params = []

    if nis:
        query += " AND (a.nis LIKE %s OR c.Nama LIKE %s)"
        params.extend([f'%{nis}%', f'%{nis}%'])
    
    if mapel:
        query += " AND b.nama_mapel=%s"
        params.append(mapel)
    
    if semester:
        query += " AND a.Semester=%s"
        params.append(semester)
    
    if tahun:
        query += " AND a.tahun_ajaran=%s"
        params.append(tahun)

    cursor.execute(query, params)
    students = cursor.fetchall()

    if not students:
        flash('Tidak ada data untuk dicetak', 'warning')
        return redirect(url_for('index'))

    cursor.close()
    conn.close()

    timestamp = date.today().strftime("%Y%m%d")
    base_folder = os.path.join("raport_siswa", f"Cetak_Semua_{timestamp}")
    os.makedirs(base_folder, exist_ok=True)
    
    created_files = []
    class_folders = {}
    
    for student in students:
        kelas = student['nama_kelas']
        
        if kelas not in class_folders:
            kelas_folder = os.path.join(base_folder, kelas)
            os.makedirs(kelas_folder, exist_ok=True)
            class_folders[kelas] = kelas_folder
        
        pdf_file = generate_student_pdf_to_folder(
            student['nis'], 
            student['Nama'],
            student['Semester'], 
            student['tahun_ajaran'],
            class_folders[kelas]
        )
        created_files.append(pdf_file)
    
    total_files = len(created_files)
    total_classes = len(class_folders)
    
    flash(f'Berhasil mencetak {total_files} rapor untuk {total_classes} kelas', 'success')
    
    return redirect(url_for('index'))


def generate_student_pdf_to_folder(nis, nama, semester, tahun, folder_path):
    def row_height(pdf, text, width, line_height):
        text = str(text)
        if not text:
            return line_height
        nb_lines = pdf.get_string_width(text) / width
        return max(line_height, (int(nb_lines) + 1) * line_height)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.Nama, c.tgl_lahir, k.nama_kelas AS kelas, a.nis, b.nama_mapel,
               a.nilai_tugas, a.nilai_uts, a.nilai_uas,
               a.nilai_akhir, a.Deskripsi
        FROM nilai_alif a
        JOIN mapel_alif b ON a.id_mapel=b.id_mapel
        JOIN siswa_alif c ON a.nis=c.nis
        JOIN kelas_alif k ON c.id_kelas=k.id_kelas
        WHERE a.nis=%s AND a.Semester=%s AND a.tahun_ajaran=%s
    """, (nis, semester, tahun))

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)

    pdf.set_font('DejaVu', '', 14)
    pdf.cell(0, 8, 'LAPORAN HASIL BELAJAR', ln=True, align='C')
    pdf.set_font('DejaVu', '', 11)
    pdf.cell(0, 6, 'SMK Negeri 2 Cimahi', ln=True, align='C')
    pdf.set_font('DejaVu', '', 8)
    pdf.cell(0, 4, ' Jl. Kamarung KM. 1,5 No. 69, Kelurahan Citeureup, Kecamatan Cimahi Utara, Kota Cimahi, Jawa Barat', ln=True, align='C')
    pdf.ln(6)

    if data:
        tgl_lahir = data[0]["tgl_lahir"]
        kelas = data[0]["kelas"]
        pdf.cell(40, 6, 'NIS', 0)
        pdf.cell(0, 6, f': {nis}', ln=True)
        pdf.cell(40, 6, 'Nama', 0)
        pdf.cell(0, 6, f': {data[0]["Nama"]}', ln=True)
        pdf.cell(40, 6, 'Tanggal Lahir', 0)
        pdf.cell(0, 6, f': {tgl_lahir}', ln=True)
        pdf.cell(40, 6, 'Kelas', 0)
        pdf.cell(0, 6, f': {kelas}', ln=True)  
        pdf.cell(40, 6, 'Semester', 0)
        pdf.cell(0, 6, f': {semester}', ln=True)
        pdf.cell(40, 6, 'Tahun Ajaran', 0)
        pdf.cell(0, 6, f': {tahun}', ln=True)

    pdf.ln(6)

    pdf.set_font('DejaVu', '', 10)
    pdf.cell(10, 8, 'No', 1, 0, 'C')
    pdf.cell(50, 8, 'Mata Pelajaran', 1, 0, 'C')
    pdf.cell(20, 8, 'Tugas', 1, 0, 'C')
    pdf.cell(20, 8, 'UTS', 1, 0, 'C')
    pdf.cell(20, 8, 'UAS', 1, 0, 'C')
    pdf.cell(25, 8, 'Nilai Akhir', 1, 0, 'C')
    pdf.cell(45, 8, 'Deskripsi', 1, 1, 'C')

    no = 1
    for d in data:
        line_height = 8
        row_h = row_height(pdf, d['Deskripsi'], 45, line_height)

        if pdf.get_y() + row_h > 270:
            pdf.add_page()
            pdf.set_font('DejaVu', '', 10)
            pdf.cell(10, 8, 'No', 1, 0, 'C')
            pdf.cell(50, 8, 'Mata Pelajaran', 1, 0, 'C')
            pdf.cell(20, 8, 'Tugas', 1, 0, 'C')
            pdf.cell(20, 8, 'UTS', 1, 0, 'C')
            pdf.cell(20, 8, 'UAS', 1, 0, 'C')
            pdf.cell(25, 8, 'Nilai Akhir', 1, 0, 'C')
            pdf.cell(45, 8, 'Deskripsi', 1, 1, 'C')

        x = pdf.get_x()
        y = pdf.get_y()

        pdf.cell(10, row_h, str(no), 1, 0, 'C')
        pdf.cell(50, row_h, d['nama_mapel'], 1, 0)
        pdf.cell(20, row_h, str(d['nilai_tugas']), 1, 0, 'C')
        pdf.cell(20, row_h, str(d['nilai_uts']), 1, 0, 'C')
        pdf.cell(20, row_h, str(d['nilai_uas']), 1, 0, 'C')
        pdf.cell(25, row_h, str(d['nilai_akhir']), 1, 0, 'C')

        pdf.set_xy(x + 145, y)
        pdf.multi_cell(45, line_height, d['Deskripsi'], 1)

        pdf.set_xy(x, y + row_h)
        no += 1

    pdf.ln(15)
    pdf.cell(0, 6, 'Mengetahui,', ln=True)

    pdf.ln(15)
    pdf.cell(90, 6, 'Wali Kelas', 0, 0, 'C')
    pdf.cell(0, 6, 'Kepala Sekolah', 0, 1, 'C')

    pdf.ln(20)
    pdf.cell(90, 6, '(............................)', 0, 0, 'C')
    pdf.cell(0, 6, '(............................)', 0, 1, 'C')

    filename = f"Rapor_{nama}_{nis}_Sem{semester}_{tahun}.pdf"
    filepath = os.path.join(folder_path, filename)
    pdf.output(filepath)
    
    return filepath

if __name__ == '__main__':
    app.run(debug=True)