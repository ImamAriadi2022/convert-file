import subprocess
import os

def compress_pdf(input_file_path, output_file_path, power=3):
    """
    Mengompres PDF menggunakan Ghostscript.
    Power menentukan tingkat kompresi dan kualitas:
    0: default (kualitas layar, ukuran sedang)
    1: printer (kualitas tinggi, ukuran lebih besar)
    2: ebook (kualitas sedang, ukuran lebih kecil)
    3: screen (kualitas rendah, ukuran paling kecil, mungkin tidak cocok untuk semua PDF)
    """
    quality = {
        0: '/default',
        1: '/printer',
        2: '/ebook',
        3: '/screen'
    }

    # Pastikan path Ghostscript (gs) ada di PATH environment variable Anda
    # atau ganti 'gs' dengan path lengkap ke executable Ghostscript
    gs_command = r"C:\Program Files\gs\gs10.05.1\bin\gswin64c.exe"

    try:
        print(f"Memulai kompresi PDF: {input_file_path}")
        print(f"Target output: {output_file_path}")
        print(f"Menggunakan level kualitas: {quality.get(power, '/default')} ({power})")

        command = [
            gs_command,
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            f'-dPDFSETTINGS={quality.get(power, "/default")}',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_file_path}',
            input_file_path
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            input_size = os.path.getsize(input_file_path) / (1024 * 1024) # MB
            output_size = os.path.getsize(output_file_path) / (1024 * 1024) # MB
            print(f"Kompresi berhasil!")
            print(f"Ukuran asli: {input_size:.2f} MB")
            print(f"Ukuran setelah kompresi: {output_size:.2f} MB")
            print(f"Rasio kompresi: {(input_size - output_size) / input_size * 100:.2f}%")
        else:
            print("Error saat kompresi PDF:")
            print("Stdout:", stdout.decode())
            print("Stderr:", stderr.decode())
            if "Unrecoverable error" in stderr.decode() or "An error occurred" in stderr.decode():
                print("\nPastikan Ghostscript terinstal dengan benar dan path ke 'gs' sudah benar atau ada di sistem PATH Anda.")
                print("Jika Anda menggunakan Windows, Anda mungkin perlu mengganti 'gs' dengan path lengkap ke gswin64c.exe atau gswin32c.exe.")

    except FileNotFoundError:
        print(f"Error: Perintah '{gs_command}' tidak ditemukan. Pastikan Ghostscript terinstal dan ada di PATH environment variable Anda.")
        print("Contoh path Ghostscript di Windows: r'C:\\Program Files\\gs\\gsX.YY\\bin\\gswin64c.exe'")
        print("Contoh path Ghostscript di Linux/macOS: 'gs'")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def compress_until_target(input_file, output_file, min_mb=5, max_mb=10):
    """
    Kompres PDF dengan berbagai level sampai ukuran output di antara min_mb dan max_mb.
    Jika tidak bisa, rekomendasikan hasil kompresi terkecil.
    """
    best_size = None
    best_file = None
    for power in [3, 2, 1, 0]:
        temp_output = f"temp_power{power}.pdf"
        compress_pdf(input_file, temp_output, power=power)
        if os.path.exists(temp_output):
            size_mb = os.path.getsize(temp_output) / (1024 * 1024)
            print(f"Level {power}: {size_mb:.2f} MB")
            # Simpan hasil terkecil
            if best_size is None or size_mb < best_size:
                best_size = size_mb
                best_file = temp_output
            if min_mb <= size_mb <= max_mb:
                os.rename(temp_output, output_file)
                print(f"Berhasil: File dikompresi ke {size_mb:.2f} MB pada level {power}.")
                # Hapus file sementara lain
                for p in [3, 2, 1, 0]:
                    t = f"temp_power{p}.pdf"
                    if t != output_file and os.path.exists(t):
                        os.remove(t)
                return
            else:
                # Jangan hapus file terkecil
                if temp_output != best_file:
                    os.remove(temp_output)
    # Jika tidak ada yang memenuhi target
    if best_file and os.path.exists(best_file):
        os.rename(best_file, output_file)
        print(f"Tidak bisa mencapai target ukuran {min_mb}-{max_mb} MB dengan preset yang ada.")
        print(f"Ukuran terkecil yang bisa dicapai: {best_size:.2f} MB. File hasil kompresi disimpan sebagai '{output_file}'.")
    else:
        print("Kompresi gagal untuk semua preset.")
    """
    Kompres PDF dengan berbagai level sampai ukuran output di antara min_mb dan max_mb.
    """
    for power in [3, 2, 1, 0]:
        temp_output = f"temp_power{power}.pdf"
        compress_pdf(input_file, temp_output, power=power)
        if os.path.exists(temp_output):
            size_mb = os.path.getsize(temp_output) / (1024 * 1024)
            print(f"Level {power}: {size_mb:.2f} MB")
            if min_mb <= size_mb <= max_mb:
                os.rename(temp_output, output_file)
                print(f"Berhasil: File dikompresi ke {size_mb:.2f} MB pada level {power}.")
                # Hapus file sementara lain
                for p in [3, 2, 1, 0]:
                    t = f"temp_power{p}.pdf"
                    if t != output_file and os.path.exists(t):
                        os.remove(t)
                return
            else:
                os.remove(temp_output)
    print("Tidak bisa mencapai target ukuran dengan preset yang ada.")

if __name__ == "__main__":
    file_input = "Materi_14_8_slide_per_page.pdf"  # Ganti dengan nama file PDF Anda
    file_output = "Materi_14_8_slide_per_page_terkompresi.pdf" # Nama file PDF hasil kompresi

    if not os.path.exists(file_input):
        print(f"File input '{file_input}' tidak ditemukan. Silakan periksa kembali nama dan lokasinya.")
    else:
        compress_until_target(file_input, file_output, min_mb=5, max_mb=10)