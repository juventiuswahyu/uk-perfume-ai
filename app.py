import streamlit as st
from groq import Groq

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Perfume Pitch Simulator - Shark Tank",
    page_icon="🧴",
    layout="wide"
)

# Custom CSS untuk tampilan elegan khas bisnis parfum
st.markdown("""
<style>
    .main-header {
        font-size: 2.6rem;
        font-weight: 700;
        color: #6B21A8;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 25px;
    }
    .status-invested {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 20px;
        border-radius: 12px;
        font-weight: bold;
        text-align: center;
        font-size: 1.8rem;
        border: 2px solid #34D399;
        margin-bottom: 15px;
    }
    .status-rejected {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 20px;
        border-radius: 12px;
        font-weight: bold;
        text-align: center;
        font-size: 1.8rem;
        border: 2px solid #F87171;
        margin-bottom: 15px;
    }
    .rocket-anim {
        font-size: 3rem;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar - Pengaturan API Key & Model Groq
st.sidebar.header("🧴 Pengaturan Simulator")
api_key = st.sidebar.text_input("Masukkan Groq API Key:", type="password")

model_option = st.sidebar.selectbox(
    "Pilih Model LLM Groq:",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "openai/gpt-oss-20b"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Cara Menggunakan:**
1. Masukkan API Key Groq Anda.
2. Tulis naskah pitch bisnis parfum/produk Anda.
3. Klik tombol **Uji Pitching**.
4. Investor AI akan mengevaluasi apakah bisnis Anda layak dapat status **INVESTED** 🚀
""")

# 3. Header Utama Aplikasi
st.markdown("<div class='main-header'>🧴 Perfume Pitch Simulator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Uji Ide & Strategi Bisnis Parfum Anda di Hadapan Investor Shark Tank AI</div>", unsafe_allow_html=True)

# 4. Form Input Pitching
with st.form("pitch_form"):
    product_name = st.text_input("Nama Produk / Brand Parfum:", placeholder="Contoh: L'Aura Luxury Fragrance")
    pitch_text = st.text_area(
        "Naskah Pitching Bisnis Parfum Anda:",
        height=200,
        placeholder="Jelaskan aroma khas (notes), target pasar, harga jual, COGS, strategi pemasaran, dan traksi penjualan saat ini..."
    )
    submit_button = st.form_submit_button("🚀 Kirim Pitching ke Investor", use_container_width=True)

# 5. Proses Evaluasi dengan Groq LLM
if submit_button:
    if not api_key:
        st.error("⚠️ Mohon masukkan Groq API Key terlebih dahulu di sidebar kiri.")
    elif not pitch_text.strip():
        st.warning("⚠️ Mohon tuliskan naskah pitching Anda.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # System prompt disesuaikan untuk bisnis parfum & output status INVESTED
            system_prompt = """
            Anda adalah juri investor ketat dan profesional dalam acara 'Shark Tank' yang ahli dalam industri parfum & keharuman (fragrance/cosmetics).
            Tugas Anda adalah mengevaluasi pitch bisnis parfum yang diberikan oleh user.
            
            Analisis pitch berdasarkan:
            1. Keunikan Produk & Keunggulan Aroma (Unique Value Proposition).
            2. Kejelasan Angka Bisnis (Harga, HPP/COGS, Margin Keuntungan, Traksi Penjualan).
            3. Potensi Pasar & Strategi Pemasaran.
            
            Format Output WAJIB mengandung salah satu dari dua keputusan utama di baris paling awal:
            - Jika pitch bagus dan layak mendapa bantuan modal/mitra: Tuliskan status [INVESTED]
            - Jika pitch buruk, angka tidak masuk akal, atau tidak unik: Tuliskan status [REJECTED - DITOLAK]
            
            Setelah keputusan tersebut, berikan analisis mendalam dan alasan rinci dari sudut pandang investor.
            """

            user_prompt = f"Nama Produk: {product_name}\n\nNaskah Pitching:\n{pitch_text}"

            with st.spinner("🤖 Investor Shark Tank sedang menganalisis bisnis parfum Anda..."):
                response = client.chat.completions.create(
                    model=model_option,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                result_text = response.choices[0].message.content

            # 6. Tampilkan Hasil
            st.markdown("---")
            st.subheader("📋 Keputusan & Evaluasi Investor")

            # Cek status Keputusan
            if "INVESTED" in result_text.upper() and "REJECTED" not in result_text.upper():
                # EFEK ROKET 🚀
                st.toast("🚀 DEAL! Selamat, proposal Anda berhasil mendapatkan status INVESTED!", icon="🚀")
                st.markdown("<div class='rocket-anim'>🚀 💨 🌌 🚀</div>", unsafe_allow_html=True)
                st.markdown("<div class='status-invested'>🎉 STATUS: INVESTED 🎉</div>", unsafe_allow_html=True)
                st.snow() # Efek salju/selebrasi segar
            else:
                st.markdown("<div class='status-rejected'>❌ STATUS: REJECTED (DITOLAK) ❌</div>", unsafe_allow_html=True)

            # Tampilkan ulasan rinci dari AI
            st.write(result_text)

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat mengontak model ({model_option}): {str(e)}")
```eof

### Perubahan Utama:
- **Ikon & Tema**: Menggunakan emoji parfum (`🧴`) pada title, icon, dan header aplikasi.
- **Efek Roket (Replacing Balloons)**: Menggunakan kombinasi `st.toast("🚀 ...")`, animasi emoji roket `🚀 💨 🌌`, dan efek `st.snow()` saat keputusan **INVESTED**.
- **Status 'INVESTED'**: Seluruh teks acuan modal 500 juta telah disederhanakan menjadi indikator status **`INVESTED`**.

Silakan coba jalankan aplikasi Streamlit Anda!
