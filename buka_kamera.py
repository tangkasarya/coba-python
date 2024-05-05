import cv2

# Fungsi untuk membuka kamera laptop
def buka_kamera():
    # Inisialisasi objek kamera
    cap = cv2.VideoCapture(0)

    # Periksa apakah kamera berhasil dibuka
    if not cap.isOpened():
        print("Tidak dapat membuka kamera.")
        return

    # Loop terus-menerus untuk membaca dan menampilkan gambar dari kamera
    while True:
        # Baca frame dari kamera
        ret, frame = cap.read()

        # Periksa apakah frame berhasil dibaca
        if not ret:
            print("Gagal membaca frame dari kamera.")
            break

        # Tampilkan frame dalam jendela
        cv2.imshow('Kamera Laptop', frame)

        # Tunggu tombol keyboard "q" ditekan untuk keluar dari loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Setelah selesai, lepaskan kamera dan tutup jendela
    cap.release()
    cv2.destroyAllWindows()

# Panggil fungsi untuk membuka kamera
buka_kamera()
