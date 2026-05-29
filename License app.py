import streamlit as st
import time

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Auto-Analyzer Organik", page_icon="🧪", layout="wide")

st.title("🧪 Auto-Analyzer Senyawa Organik")
st.write("Pilih golongan senyawa organik. Sistem akan otomatis mereaksikannya secara berurutan dengan 8 pereaksi standar laboratorium.")

st.divider()

# Input Senyawa Utama
senyawa = st.selectbox(
    "Masukkan Golongan Senyawa:",
    ["-- Pilih Senyawa --", "Alkohol Primer", "Alkohol Sekunder", "Alkohol Tersier", "Aldehid", "Keton", "Asam Karboksilat", "Alkana"]
)

# Database Logika Reaksi Berurutan
database_reaksi = {
    "Alkohol Primer": {
        "Ceric Nitrat": {"hasil": "(+) Merah", "alasan": "Gugus -OH alifatik membentuk kompleks merah dengan ion Cerium."},
        "Pereaksi Jones": {"hasil": "(+) Jingga ke Hijau", "alasan": "Dioksidasi menjadi aldehid, lalu asam karboksilat. Cr(VI) tereduksi menjadi Cr(III)."},
        "Pereaksi Lucas": {"hasil": "(-) Bening", "alasan": "Karbokation primer sangat tidak stabil; tidak bereaksi pada suhu ruang."},
        "Uji Iodoform": {"hasil": "(-) Negatif / (+) Etanol", "alasan": "Secara umum negatif, kecuali senyawa spesifik Etanol yang menghasilkan endapan kuning."},
        "Na-Bisulfit": {"hasil": "(-) Bening", "alasan": "Tidak memiliki gugus karbonil reaktif untuk adisi nukleofilik."},
        "Pereaksi Fehling": {"hasil": "(-) Tetap Biru", "alasan": "Gugus hidroksil tidak dapat mereduksi ion tembaga(II)."},
        "Hidroksilamin": {"hasil": "(-) Negatif", "alasan": "Hanya bereaksi dengan gugus karbonil untuk membentuk oksim."},
        "KMnO4": {"hasil": "(+) Pudar / Endapan Coklat", "alasan": "Gugus alkohol primer dioksidasi kuat menjadi asam karboksilat."}
    },
    "Alkohol Sekunder": {
        "Ceric Nitrat": {"hasil": "(+) Merah", "alasan": "Gugus -OH alifatik berkoordinasi membentuk kompleks merah."},
        "Pereaksi Jones": {"hasil": "(+) Jingga ke Hijau", "alasan": "Dioksidasi menjadi keton. Cr(VI) tereduksi menjadi Cr(III)."},
        "Pereaksi Lucas": {"hasil": "(+) Keruh (5-10 menit)", "alasan": "Reaksi SN1 berjalan lambat membentuk endapan alkil klorida."},
        "Uji Iodoform": {"hasil": "(+) Jika Metil Karbinol", "alasan": "Menghasilkan endapan kuning iodoform HANYA JIKA struktur alkoholnya memiliki gugus metil di sebelah -OH (contoh: 2-butanol)."},
        "Na-Bisulfit": {"hasil": "(-) Bening", "alasan": "Tidak memiliki gugus karbonil bebas."},
        "Pereaksi Fehling": {"hasil": "(-) Tetap Biru", "alasan": "Tidak memiliki kemampuan reduktor yang cukup kuat."},
        "Hidroksilamin": {"hasil": "(-) Negatif", "alasan": "Tidak ada gugus karbonil bebas."},
        "KMnO4": {"hasil": "(+) Pudar / Endapan Coklat", "alasan": "Dioksidasi kuat membentuk keton, memudarkan warna ungu KMnO4."}
    },
    "Alkohol Tersier": {
        "Ceric Nitrat": {"hasil": "(+) Merah", "alasan": "Gugus -OH bebas bereaksi membentuk kompleks merah."},
        "Pereaksi Jones": {"hasil": "(-) Tetap Jingga", "alasan": "Tidak memiliki hidrogen alfa; tidak dapat dioksidasi."},
        "Pereaksi Lucas": {"hasil": "(+) Keruh Seketika", "alasan": "Karbokation tersier sangat stabil; substitusi pembentukan alkil klorida terjadi sangat cepat."},
        "Uji Iodoform": {"hasil": "(-) Bening", "alasan": "Tidak memiliki hidrogen yang dapat dioksidasi membentuk metil keton."},
        "Na-Bisulfit": {"hasil": "(-) Bening", "alasan": "Bukan golongan karbonil."},
        "Pereaksi Fehling": {"hasil": "(-) Tetap Biru", "alasan": "Tidak memiliki gugus pereduksi."},
        "Hidroksilamin": {"hasil": "(-) Negatif", "alasan": "Bukan senyawa karbonil."},
        "KMnO4": {"hasil": "(-) Tetap Ungu", "alasan": "Kebal terhadap oksidator kuat karena ketiadaan hidrogen alfa."}
    },
    "Aldehid": {
        "Ceric Nitrat": {"hasil": "(-) Negatif", "alasan": "Tidak memiliki gugus -OH alkoholik."},
        "Pereaksi Jones": {"hasil": "(+) Jingga ke Hijau", "alasan": "Sangat mudah dioksidasi menjadi asam karboksilat."},
        "Pereaksi Lucas": {"hasil": "(-) Bening", "alasan": "Bukan golongan alkohol."},
        "Uji Iodoform": {"hasil": "(-) Negatif / (+) Asetaldehida", "alasan": "Secara umum negatif, HANYA asetaldehida yang merespon positif endapan kuning."},
        "Na-Bisulfit": {"hasil": "(+) Endapan Putih", "alasan": "Gugus karbonil ujung sangat mudah mengalami adisi nukleofilik oleh bisulfit."},
        "Pereaksi Fehling": {"hasil": "(+) Endapan Merah Bata", "alasan": "Reduktor kuat; mereduksi ion Cu(II) menjadi Cu(I) oksida."},
        "Hidroksilamin": {"hasil": "(+) Kristal Oksim", "alasan": "Berkondensasi dengan gugus karbonil membentuk senyawa oksim."},
        "KMnO4": {"hasil": "(+) Pudar / Endapan Coklat", "alasan": "Mudah dioksidasi oleh permanganat menjadi asam karboksilat."}
    },
    "Keton": {
        "Ceric Nitrat": {"hasil": "(-) Negatif", "alasan": "Tidak memiliki gugus -OH."},
        "Pereaksi Jones": {"hasil": "(-) Tetap Jingga", "alasan": "Tidak memiliki hidrogen alfa pada karbonil; tidak dapat dioksidasi."},
        "Pereaksi Lucas": {"hasil": "(-) Bening", "alasan": "Pereaksi spesifik alkohol."},
        "Uji Iodoform": {"hasil": "(+) Jika Metil Keton", "alasan": "Menghasilkan endapan kuning HANYA JIKA keton memiliki gugus metil (contoh: aseton)."},
        "Na-Bisulfit": {"hasil": "(+) Endapan Putih (Keton Kecil)", "alasan": "Hanya terjadi pada keton dengan halangan sterik rendah (seperti aseton)."},
        "Pereaksi Fehling": {"hasil": "(-) Tetap Biru", "alasan": "Tidak memiliki daya reduktor untuk mereduksi Fehling."},
        "Hidroksilamin": {"hasil": "(+) Kristal Oksim", "alasan": "Adisi eliminasi pada karbonil membentuk senyawa oksim."},
        "KMnO4": {"hasil": "(-) Tetap Ungu", "alasan": "Tahan terhadap oksidasi normal."}
    },
    "Asam Karboksilat": {
        "Ceric Nitrat": {"hasil": "(-) Negatif", "alasan": "Gugus karboksil sangat menarik elektron, atom O kurang nukleofilik untuk mengikat Cerium."},
        "Pereaksi Jones": {"hasil": "(-) Tetap Jingga", "alasan": "Sudah berada dalam tingkat oksidasi maksimal."},
        "Pereaksi Lucas": {"hasil": "(-) Bening", "alasan": "Bukan alkohol alifatik."},
        "Uji Iodoform": {"hasil": "(-) Bening", "alasan": "Tidak membentuk struktur metil keton basa."},
        "Na-Bisulfit": {"hasil": "(-) Bening", "alasan": "Efek resonansi membuat karbon karboksilat tidak cukup positif untuk diadisi."},
        "Pereaksi Fehling": {"hasil": "(-) Tetap Biru", "alasan": "Tidak memiliki sifat reduktor."},
        "Hidroksilamin": {"hasil": "(-) Negatif", "alasan": "Gugus karbonil pada asam karboksilat dilindungi oleh resonansi, sulit membentuk oksim."},
        "KMnO4": {"hasil": "(-) Tetap Ungu", "alasan": "Sudah dioksidasi penuh."}
    },
    "Alkana": {
        "Ceric Nitrat": {"hasil": "(-) Negatif", "alasan": "Hanya terdiri dari ikatan C-C dan C-H tunggal (inert)."},
        "Pereaksi Jones": {"hasil": "(-) Tetap Jingga", "alasan": "Tidak ada gugus fungsional reaktif."},
        "Pereaksi Lucas": {"hasil": "(-) Bening", "alasan": "Senyawa non-polar dan inert."},
        "Uji Iodoform": {"hasil": "(-) Bening", "alasan": "Senyawa inert."},
        "Na-Bisulfit": {"hasil": "(-) Bening", "alasan": "Senyawa inert."},
        "Pereaksi Fehling": {"hasil": "(-) Tetap Biru", "alasan": "Senyawa inert."},
        "Hidroksilamin": {"hasil": "(-) Negatif", "alasan": "Senyawa inert."},
        "KMnO4": {"hasil": "(-) Tetap Ungu", "alasan": "Alkana jenuh kebal terhadap oksidator."}
    }
}

urutan_pereaksi = [
    "Ceric Nitrat", "Pereaksi Jones", "Pereaksi Lucas", 
    "Uji Iodoform", "Na-Bisulfit", "Pereaksi Fehling", 
    "Hidroksilamin", "KMnO4"
]

if st.button("Reaksikan Secara Berurutan 🚀", type="primary"):
    if senyawa == "-- Pilih Senyawa --":
        st.warning("⚠️ Harap pilih senyawa terlebih dahulu!")
    else:
        st.write(f"### 🧪 Memproses: **{senyawa}**")
        st.progress(0)
        
        # Penampung hasil menggunakan grid
        cols = st.columns(2)
        
        for i, pereaksi in enumerate(urutan_pereaksi):
            # Efek delay untuk mensimulasikan waktu reaksi laboratorium
            with st.spinner(f"Sedang mereaksikan dengan {pereaksi}..."):
                time.sleep(0.6) 
            
            data_reaksi = database_reaksi[senyawa][pereaksi]
            hasil = data_reaksi["hasil"]
            alasan = data_reaksi["alasan"]
            
            # Membagi output ke kolom kiri dan kanan secara berurutan
            col_target = cols[i % 2]
            
            with col_target:
                if "(+)" in hasil:
                    st.success(f"**{i+1}. {pereaksi}**\n\n**Hasil:** {hasil}\n\n**Analisis:** {alasan}")
                else:
                    st.error(f"**{i+1}. {pereaksi}**\n\n**Hasil:** {hasil}\n\n**Analisis:** {alasan}")
                    
            # Mengupdate garis progres di atas
            st.progress((i + 1) / len(urutan_pereaksi))
            
        st.write("---")
        st.info("✅ **Proses Identifikasi Selesai.** Kesimpulan sifat reaktivitas telah dicatat sepenuhnya.")
