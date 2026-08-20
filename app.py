import streamlit as st
from groq import Groq

st.set_page_config(page_title="UK AI Perfume Investor", page_icon="🧴", layout="centered")

st.title("🧴 UK AI Perfume Investor")
st.write("AI Promosi Sekolah Universitas Karangturi Semarang")

# Form Input Pitching
with st.form("pitch_form"):
    team_name = st.text_input("Brand Name / Nama Kelompok", placeholder="Contoh: English Pear Elegance")
    target_market = st.text_input("Targeting", placeholder="Contoh: Mahasiswi Gen Z usia 18-22 tahun yang suka gaya minimalis-elegan")
    
    st.subheader("🧪 Fragrance Pyramid (Aroma Hasil Blind Test)")
    top_notes = st.text_input("Top Notes", placeholder="Aroma awal saat disemprot")
    middle_notes = st.text_input("Middle Notes", placeholder="Aroma inti/jantung parfum")
    base_notes = st.text_input("Base Notes", placeholder="Aroma dasar yang bertahan lama")
    
    st.subheader("📢 Copywriting & Promosi")
    copywriting = st.text_area("Teks Copywriting Complete (Caption IG/TikTok)", height=180, placeholder="Tuliskan caption promosi lengkapmu di sini...")
    
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

                **SKEMA SKOR TOTAL (SKOR MAKSIMAL 100):**
                1. Brand Name (Bobot 20%): Keunikan, daya ingat (*ear-catching*), dan relevansi.
                2. Targeting (Bobot 20%): Spesifikasi dan kejelasan profil audiens sasaran.
                3. Akurasi Aroma (Bobot MAKSIMAL 15% SAJA): Keakuratan tebakan aroma siswa dibanding Racikan Asli. (Catatan: Jika aroma meleset, skor bagian ini kecil, NAMUN kelompok TETAP BISA DAPAT STATUS [INVESTED] jika skor aspek marketing lainnya sangat tinggi!).
                4. Bedah Copywriting (Bobot 45%): Penilaian tajam pada Hook, Brand Voice, Localization, dan Call to Action (CTA).

                **KRITERIA KEPUTUSAN:**
                - STATUS [INVESTED]: Jika Skor Total >= 70 (Meskipun akurasi aroma meleset, jika marketingnya sangat kuat hingga mencapai skor total 70+, tetap beri status INVESTED!).
                - STATUS [REJECTED - DITOLAK]: Jika Skor Total < 70.

                **FORMAT OUTPUT (Gunakan Markdown):**
                1. **STATUS INVESTASI**: Pilih antara [INVESTED] atau [REJECTED - DITOLAK] disertai komentar tajam dan membakar semangat.
                2. **SKOR TOTAL**: Berikan angka total 1-100 dan sertakan rincian poinnya (Brand Name: x/20, Targeting: x/20, Akurasi Aroma: x/15, Marketing: x/45).
                3. **PEMBEDAHAN COPYWRITING**: Ulas secara mendalam komponen Hook, Brand Voice, Localization, dan CTA dari teks iklan siswa.
                4. **AROMA SEBENARNYA vs TEBAKAN SISWA**: Tampilkan perbandingan tebakan siswa dengan racikan asli.
                5. **MASUKAN EVALUASI**: 1-2 saran konkret untuk perbaikan.
                """
                
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="openai/gpt-oss-20b",
                )
                
                st.success("Analisis AI Investor Selesai!")
                st.markdown(response.choices[0].message.content)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan pada sistem: {e}")
