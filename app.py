import streamlit as st
from groq import Groq

st.set_page_config(page_title="Sedes AI Perfume Investor", page_icon="💼", layout="centered")

st.title("💼 Sedes AI Perfume Investor")
st.write("Sampaikan ide *marketing* dan *copywriting* parfum kelompokmu. Lihat apakah AI Investor tertarik mendanai brand-mu!")

with st.form("pitch_form"):
    team_name = st.text_input("Nama Kelompok / Brand Parfum")
    target_market = st.text_input("Target Market (Contoh: Anak skena, Gen Z, Skena Kpop, dll)")
    scent_notes = st.text_input("Aroma Hasil Blind Test (Contoh: Vanila manis, Segar sitrus, Citrus smoky)")
    copywriting = st.text_area("Teks Copywriting / Caption Promosi Instagram/TikTok", height=150)
    
    submitted = st.form_submit_button("🚀 Submit Pitch Ke Investor")

if submitted:
    if not copywriting or not team_name:
        st.warning("⚠️ Mohon isi Nama Kelompok dan Teks Copywriting secara lengkap!")
    else:
        try:
            groq_key = st.secrets["GROQ_API_KEY"]
            client = Groq(api_key=groq_key)
            
            with st.spinner("AI Investor sedang menganalisis pitch-mu..."):
                prompt = f"""
                Kamu adalah Venture Capitalist & Marketing Director Senior yang berpengalaman di industri perfumery.
                Tugasmu adalah menilai hasil karya siswa SMA berikut:
                
                - Nama Brand: {team_name}
                - Target Market: {target_market}
                - Karakter Aroma (Blind Test): {scent_notes}
                - Copywriting / Promosi: {copywriting}
                
                Berikan respon dengan format berikut (gunakan Markdown):
                1. **STATUS INVESTASI**: Pilih antara [INVESTED Rp 500 JUTA] atau [REJECTED - DITOLAK] dengan gaya bahasa lugas tapi membakar semangat.
                2. **SKOR MARKETING**: Berikan nilai angka 1-100.
                3. **ULASAN COPYWRITING**: Apa kelebihan dari narasi mereka? (Apakah hook-nya dapet, emosinya kena, dll).
                4. **MASUKAN EVALUASI**: 1-2 saran konkret untuk perbaikan iklan mereka.
                
                Gunakan nada bicara profesional, sedikit humor, dan relevan untuk anak SMA (Gen Z).
                """
                
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-70b-8192",
                )
                
                st.balloons()
                st.success("Analisis AI Investor Selesai!")
                st.markdown(response.choices[0].message.content)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan pada sistem: {e}")
