from flask import Flask, render_template, request

app = Flask(__name__)

#fungsi untuk ubah format angka Indonesia ke integer
def parse_rupiah(angka):
    try:
        if not angka:
            return 0
        angka = angka.replace(".", "").replace(",", "")
        return int(angka)
    except:
        return 0

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None
    status = None

    if request.method == "POST":
        try:
            # ambil & bersihkan gaji
            gaji_input = request.form.get("gaji")
            gaji = parse_rupiah(gaji_input)

            # ambil semua pengeluaran
            jumlah_list = request.form.getlist("jumlah_pengeluaran[]")

            total_pengeluaran = 0
            for j in jumlah_list:
                total_pengeluaran += parse_rupiah(j)

            # hitung sisa
            sisa = gaji - total_pengeluaran

            # tentukan status
            if sisa > gaji * 0.3:
                status = "AMAN"
            elif sisa > 0:
                status = "CUKUP"
            else:
                status = "BOROS"

            # simpan hasil
            hasil = {
                "gaji": gaji,
                "pengeluaran": total_pengeluaran,
                "sisa": sisa
            }

        except Exception as e:
            print("ERROR:", e)
            status = "Input tidak valid!"

    return render_template("index.html", hasil=hasil, status=status)

if __name__ == "__main__":
    app.run(debug=True)
