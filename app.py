import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

# ====================================
# LOAD DATA
# ====================================

data = pd.read_excel("data.xlsx")
data_dak = pd.read_excel("data_dak.xlsx")

# ====================================
# JUDUL
# ====================================

st.markdown(
    """
    <h1 style='text-align: center;'>
    Dashboard 
    Indeks Kinerja Sistem Irigasi
    Kewenangan Provinsi Jawa Timur
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align: center; font-size:20px;'>
    Dinas Pekerjaan Umum Sumber Daya Air Provinsi Jawa Timur
    </p>
    """,
    unsafe_allow_html=True
)

# ====================================
# FILTER DI
# ====================================

di_list = sorted(data["DI"].dropna().unique())

di = st.selectbox(
    "Cari / Pilih Daerah Irigasi",
    di_list
)

# ====================================
# FILTER TAHUN
# ====================================

# Ambil seluruh data DI
data_di_semua = data[data["DI"] == di]

tahun = st.selectbox(
    "Pilih Tahun",
    sorted(data_di_semua["Tahun"].unique())
)

# Filter berdasarkan tahun
data_di = data_di_semua[data_di_semua["Tahun"] == tahun]

# ====================================
# TAMPILKAN DATA
# ====================================

st.subheader("Data Daerah Irigasi")

# Format angka 2 digit desimal
data_tampil = data_di.copy()

kolom_angka = [
    "Fisik",
    "Produktivitas",
    "Sarana",
    "Organisasi",
    "Dokumentasi",
    "P3A",
    "IKSI"
]

for kolom in kolom_angka:
    data_tampil[kolom] = data_tampil[kolom].round(2)

st.dataframe(data_tampil)

# ====================================
# NILAI IKSI
# ====================================

iksi = float(data_di["IKSI"].values[0])

st.subheader("Nilai IKSI")

st.write("IKSI :", round(iksi,2))

# ====================================
# STATUS RISIKO
# ====================================

if iksi >= 80:
    status = "Sangat Baik"

elif iksi >= 70:
    status = "Baik"

elif iksi >= 55:
    status = "Kurang dan Perlu Perhatian"

else:
    status = "Jelek dan Perlu Perhatian"

st.subheader("Kategori Kinerja")

st.write(status)
# ====================================
# GRAFIK TREN IKSI
# ====================================

st.subheader("Tren IKSI 2021-2025")

# Ambil seluruh data DI terpilih
tren_di = data[data["DI"] == di]

# Urutkan berdasarkan tahun
tren_di = tren_di.sort_values(by="Tahun")

# Jadikan tahun sebagai index
# Ubah tahun menjadi text
tren_di["Tahun"] = tren_di["Tahun"].astype(str)

# Jadikan tahun sebagai index
chart_tren = tren_di.set_index("Tahun")

# Tampilkan grafik
st.line_chart(chart_tren["IKSI"])
# ====================================
# GRAFIK TREN FISIK
# ====================================

st.subheader("Tren IKJI 2021-2025")

st.line_chart(chart_tren["Fisik"])

iksi_sekarang = data_di["IKSI"].iloc[0]

if iksi_sekarang >= 80:
    kategori = "🟢 Kinerja Sangat Baik"
elif iksi_sekarang >= 70:
    kategori = "🔵 Kinerja Baik"
elif iksi_sekarang >= 55:
    kategori = "🟡 Kinerja Kurang dan Perlu Perhatian"
else:
    kategori = "🔴 Kinerja Jelek dan Perlu Perhatian"

st.write(kategori)
# ====================================
# ANALISIS DANA REHABILITASI
# ====================================

# ====================================
# SPASI SECTION
# ====================================

st.markdown("<br><br>", unsafe_allow_html=True)

# garis pemisah
st.markdown("---")

# ====================================
# JUDUL ANALISIS
# ====================================

st.markdown(
    """
    <h1 style='
    text-align: center;
    font-size: 52px;
    '>
    Analisis DAK dengan Peningkatan IKSI
    </h1>
    """,
    unsafe_allow_html=True
)

# Pilih DI rehabilitasi

di_dak = st.selectbox(
    "Pilih DI yang Mendapatkan DAK",
    sorted(data_dak["DI"].dropna().unique())
)

# Filter data

dak_di = data_dak[data_dak["DI"] == di_dak]

# Tampilkan data

st.subheader("Data Rehabilitasi")

# ====================================
# FORMAT TAMPILAN DATA
# ====================================

dak_tampil = dak_di.copy()

# Format rupiah
dak_tampil["Nilai_Kontrak"] = dak_tampil["Nilai_Kontrak"].apply(
    lambda x: f"Rp {x:,.0f}"
)

# Format persen
dak_tampil["Kenaikan_IKJI"] = (
    dak_tampil["Kenaikan_IKJI"] * 100
).round(2).astype(str) + "%"

dak_tampil["Kenaikan_IKSI"] = (
    dak_tampil["Kenaikan_IKSI"] * 100
).round(2).astype(str) + "%"

# Tampilkan
st.dataframe(dak_tampil)

# ====================================
# BEFORE vs AFTER REHABILITASI
# ====================================

st.subheader("Dampak Rehabilitasi terhadap Peningkatan IKSI")

# Ambil data pertama
row = dak_di.iloc[0]

# Data
iksi_sebelum = row["IKSI_Sebelum"]

iksi_sesudah = row["IKSI_Sesudah"]

kenaikan = row["Kenaikan_IKSI"] * 100

dana = row["Nilai_Kontrak"]

tahun_rehab = row["Tahun"]

# ====================================
# GRAFIK
# ====================================

fig, ax = plt.subplots(figsize=(8,5))

kategori = ["Sebelum", "Sesudah"]

nilai = [iksi_sebelum, iksi_sesudah]

bars = ax.bar(kategori, nilai)

# ====================================
# LABEL NILAI
# ====================================

for bar in bars:

    height = bar.get_height()

    ax.text(
        bar.get_x() + bar.get_width()/2,
        height + 1,
        f"{height:.2f}",
        ha='center'
    )

# ====================================
# JUDUL
# ====================================

ax.set_title(f"Dampak Rehabilitasi Tahun {tahun_rehab}")

ax.set_ylabel("Nilai IKSI")

# ====================================
# INFO TAMBAHAN
# ====================================

st.write(f"💰 Dana DAK : Rp {dana:,.0f}")

st.write(f"📈 Kenaikan IKSI : {kenaikan:.2f} %")

# ====================================
# INTERPRETASI
# ====================================

if kenaikan > 15:

    st.success(
        "Rehabilitasi memberikan peningkatan IKSI yang signifikan."
    )

elif kenaikan > 5:

    st.info(
        "Rehabilitasi memberikan peningkatan IKSI sedang."
    )

else:

    st.warning(
        "Peningkatan IKSI relatif kecil."
    )

# ====================================
# TAMPILKAN GRAFIK
# ====================================

st.pyplot(fig)
# ====================================
# IKSI JAWA TIMUR 2021-2025
# ====================================
# ====================================
# SPASI SECTION
# ====================================
# ====================================
# SPASI SECTION
# ====================================

st.markdown("<br><br>", unsafe_allow_html=True)

# garis pemisah
st.markdown("---")

# ====================================
# JUDUL SECTION
# ====================================

st.markdown(
    """
    <h1 style='
    text-align: center;
    font-size: 52px;
    '>
    Tren IKSI Jawa Timur
    dan Dana Rehabilitasi
    </h1>
    """,
    unsafe_allow_html=True
)

# ====================================
# HITUNG IKSI JATIM
# ====================================

luas_total_jatim = 167128

hasil_tahun = []

for tahun_loop in sorted(data["Tahun"].unique()):

    data_tahun = data[data["Tahun"] == tahun_loop]

    # Hitung tiap komponen
    fisik = (
        (data_tahun["Fisik"] * data_tahun["Luas"]).sum()
        / luas_total_jatim
    )

    produktivitas = (
        (data_tahun["Produktivitas"] * data_tahun["Luas"]).sum()
        / luas_total_jatim
    )

    sarana = (
        (data_tahun["Sarana"] * data_tahun["Luas"]).sum()
        / luas_total_jatim
    )

    organisasi = (
        (data_tahun["Organisasi"] * data_tahun["Luas"]).sum()
        / luas_total_jatim
    )

    dokumentasi = (
        (data_tahun["Dokumentasi"] * data_tahun["Luas"]).sum()
        / luas_total_jatim
    )

    p3a = (
        (data_tahun["P3A"] * data_tahun["Luas"]).sum()
        / luas_total_jatim
    )

    iksi_jatim = (
        fisik
        + produktivitas
        + sarana
        + organisasi
        + dokumentasi
        + p3a
    )

    # ====================================
    # TOTAL DANA DAK
    # ====================================

    data_dak_tahun = data_dak[
        data_dak["Tahun"] == tahun_loop
    ]

    total_dak = data_dak_tahun[
        "Nilai_Kontrak"
    ].sum()

    hasil_tahun.append({
        "Tahun": tahun_loop,
        "IKSI_Jatim": round(iksi_jatim,2),
        "DAK": total_dak
    })

# ====================================
# DATAFRAME
# ====================================

df_jatim = pd.DataFrame(hasil_tahun)

# ====================================
# FORMAT TAMPILAN
# ====================================

df_tampil = df_jatim.copy()

# format rupiah
df_tampil["DAK"] = df_tampil["DAK"].apply(
    lambda x: f"Rp {x:,.0f}"
)

# tampilkan
st.dataframe(df_tampil)

# ====================================
# GRAFIK
# ====================================

fig, ax = plt.subplots(figsize=(12,6))

# garis IKSI
ax.plot(
    df_jatim["Tahun"],
    df_jatim["IKSI_Jatim"],
    marker='o',
    linewidth=3
)

# label titik IKSI
for x, y in zip(
    df_jatim["Tahun"],
    df_jatim["IKSI_Jatim"]
):

    ax.text(
        x,
        y + 0.3,
        f"{y:.2f}",
        ha='center'
    )

# anotasi dana DAK
for x, dak in zip(
    df_jatim["Tahun"],
    df_jatim["DAK"]
):

    if dak > 0:

        ax.annotate(
            f"DAK\nRp {dak/1_000_000_000:.1f} M",
            (x, df_jatim[
                df_jatim["Tahun"] == x
            ]["IKSI_Jatim"].values[0]),
            textcoords="offset points",
            xytext=(0,-35),
            ha='center'
        )

# judul
ax.set_title(
    "Tren Perbandingan IKSI Jawa Timur dengan Dana Alokasi Khusus"
)

# label
ax.set_xlabel("Tahun")

ax.set_ylabel("IKSI Jawa Timur")

# ====================================
# PENGATURAN SKALA
# ====================================

# sumbu vertikal mulai dari 56
ax.set_ylim(56, 67)

# sumbu horizontal per 1 tahun
ax.set_xticks(df_jatim["Tahun"])

# tampilkan
st.pyplot(fig)
# ====================================
# SIMULASI INVESTASI IKSI
# ====================================

st.header("Simulasi Investasi dan Prediksi IKSI Jawa Timur")

# ====================================
# HITUNG EFEKTIVITAS HISTORIS
# ====================================

# gunakan data 2021-2024 saja
simulasi_data = df_jatim[df_jatim["DAK"] > 0].copy()

# hitung kenaikan IKSI tahunan
simulasi_data["Kenaikan_IKSI"] = (
    simulasi_data["IKSI_Jatim"].diff()
)

# hapus tahun pertama
simulasi_data = simulasi_data.dropna()

# efektivitas per rupiah
simulasi_data["Efektivitas"] = (
    simulasi_data["Kenaikan_IKSI"]
    /
    (simulasi_data["DAK"] / 1_000_000_000)
)

# rata-rata efektivitas
efektivitas_rata2 = (
    simulasi_data["Efektivitas"].mean()
)

# ====================================
# BASELINE IKSI 2025
# ====================================

iksi_awal = 65.83

st.write(
    f"IKSI Jawa Timur Tahun 2025 : {iksi_awal}"
)

# ====================================
# SLIDER INVESTASI
# ====================================

investasi = st.slider(
    "Simulasi Dana Rehabilitasi (Miliar Rupiah)",
    min_value=0,
    max_value=100,
    value=10
)

# ====================================
# PREDIKSI IKSI
# ====================================

kenaikan_prediksi = (
    investasi * efektivitas_rata2
)

iksi_prediksi = (
    iksi_awal + kenaikan_prediksi
)

# ====================================
# HASIL SIMULASI
# ====================================

st.subheader("Hasil Simulasi")

# ====================================
# METRIC DASHBOARD
# ====================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Investasi",
        f"Rp {investasi} M"
    )

with col2:

    st.metric(
        "Prediksi Kenaikan IKSI",
        f"{kenaikan_prediksi:.2f}"
    )

with col3:

    st.metric(
        "Prediksi IKSI Jatim",
        f"{iksi_prediksi:.2f}"
    )

# ====================================
# TARGET IKSI
# ====================================

st.subheader("Estimasi Kebutuhan Dana")

target_iksi = st.number_input(
    "Masukkan Target IKSI",
    min_value=55.0,
    max_value=100.0,
    value=70.0
)

selisih = target_iksi - iksi_awal

if selisih > 0:

    kebutuhan_dana = (
        selisih / efektivitas_rata2
    )

    st.write(
        f"Perkiraan dana yang dibutuhkan "
        f"untuk mencapai IKSI "
        f"{target_iksi:.2f}"
    )

    st.success(
        f"≈ Rp {kebutuhan_dana:.2f} Miliar"
    )

else:

    st.info(
        "Target sudah tercapai."
    )