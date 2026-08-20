import streamlit as st
from groq import Groq

st.set_page_config(page_title="Sedes AI Perfume Investor", page_icon="🧴", layout="centered")

st.title("🧴 Sedes AI Perfume Investor")
st.write("Uji pitch bisnis dan racikan parfum kelompokmu di hadapan AI Investor!")

# Form Input Pitching
with st.form("pitch_form"):
    team_name = st.text_input("Brand Name / Nama Kelompok", placeholder="Contoh: English Pear Elegance")
    target_market = st.text_input("Targeting", placeholder="Contoh: Mahasiswi Gen Z usia 18-22 tahun yang suka gaya minimalis-elegan")
    
    st.subheader("🧪 Fragrance Pyramid (Aroma Hasil Blind Test)")
    top_notes = st.text_input("Top Notes", placeholder="Aroma awal saat disemprot")
    middle_notes = st.text_input("Middle Notes", placeholder="Aroma inti/jantung parfum")
    base_notes = st.text_input("Base Notes", placeholder="Aroma dasar yang bertahan lama")
    
    st.subheader("📢 Copywriting & Promosi")
    copywriting = st.text_area("Teks Copywriting Complete (Caption IG/TikTok)", height=180, placeholder="Tuliskan caption promosi lengkapmu di sini (sertakan kalimat pembuka, pesan utama, dan ajakan bertindak)...")
    
    submitted = st.form_submit_button("🚀 Submit Pitch Ke Investor")

if submitted:
    if not copywriting or not team_name:
        st.warning("⚠️ Mohon lengkapi Nama Brand dan Copywriting!")
    else:
        try:
            groq_key = st.secrets["GROQ_API_KEY"]
            client = Groq(api_key=groq_key)
            
            with st.spinner("AI Investor sedang menganalisis pitch-mu..."):
                prompt = f"""
                Kamu adalah Venture Capitalist & Marketing Director Senior di industri perfumery.
                Tugasmu adalah menilai hasil pitch parfum siswa SMA berdasarkan masukan berikut:

                **INPUT SISWA:**
                - Nama Brand: {team_name}
                - Target Market: {target_market}
                - Top Notes Input: {top_notes}
                - Middle Notes Input: {middle_notes}
                - Base Notes Input: {base_notes}
                - Copywriting Lengkap: {copywriting}

                **PATOKAN AROMA SEBENARNYA (RACIKAN ASLI):**
                - Top Notes: English Pear, Melon
                - Middle Notes: Freesia, Rose
                - Base Notes: Patchouli, Amber, Musk

                **PANDUAN PENILAIAN:**
                1. Brand Name: Beri nilai lebih jika unik, ear-catching, dan mudah diingat.
                2. Targeting: Semakin spesifik targetnya, semakin tinggi skornya.
                3. Akurasi Aroma: Semakin cocok tebakan Top/Middle/Base Notes siswa dengan Racikan Asli, semakin tinggi skornya.
                4. Bedah Copywriting:
                   - Hook (Kalimat pembuka/penarik perhatian)
                   - Brand Voice (Gaya bahasa & konsistensi nada)
                   - Localization (Pendekatan konteks lokal/iklim/budaya)
                   - Call To Action / CTA (Kejelasan ajakan bertindak)

                **FORMAT OUTPUT (Gunakan Markdown):**
                1. **STATUS INVESTASI**: Pilih antara [INVESTED] atau [REJECTED - DITOLAK] disertai komentar tajam dan membakar semangat.
                2. **SKOR TOTAL**: Nilai 1-100 (Sebutkan rincian: Brand Name, Targeting, Akurasi Aroma, & Marketing).
                3. **PEMBEDAHAN COPYWRITING**: Ulas secara mendalam komponen Hook, Brand Voice, Localization, dan CTA dari teks iklan siswa.
                4. **AROMA SEBENARNYA vs TEBAKAN SISWA**: Tampilkan tabel/perbandingan tebakan siswa dengan racikan asli.
                5. **MASUKAN EVALUASI**: 1-2 saran konkret untuk perbaikan.
                """
                
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="openai/gpt-oss-20b",
                )
                
                st.balloons()
                st.success("Analisis AI Investor Selesai!")
                st.markdown(response.choices[0].message.content)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan pada sistem: {e}")
