import streamlit as st

def show():
    #Title
    st.markdown(
        """
        <h1 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:20px;'>
            TENTANG WEBSITE
        </h1>
        """,
        unsafe_allow_html=True
    )

    #Description
    st.markdown(
        """
        <div style='text-align: justify; font-size:16px; padding-left:50px; padding-right:50px;'>
        Website ini dikembangkan untuk menyajikan informasi mengenai kondisi wilayah di Indonesia 
        melalui proses <b>clustering</b>. Dengan mengunggah dataset sesuai format, pengguna dapat 
        melihat bagaimana kabupaten/kota dikelompokkan berdasarkan indikator tertentu seperti 
        Angka Harapan Hidup (AHH), Persentase Penduduk Miskin (P0), Indeks Kedalaman Kemiskinan (P1), 
        Indeks Keparahan Kemiskinan (P2), dan Rata-Rata Lama Sekolah (RLS). 
        <br><br>
        Hasil yang ditampilkan berupa tabel, grafik, serta peta interaktif yang dapat diunduh. 
        Dengan demikian, website ini bermanfaat sebagai informasi untuk memahami perbedaan antarwilayah, 
        mendukung analisis, maupun dijadikan referensi bagi penelitian dan pengambilan keputusan.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
        
    st.markdown(
        """
        <p style='text-align: justify; font-size:16px; padding-left:50px; padding-right:50px;'>
        Jika membutuhkan informasi lebih lanjut atau memiliki pertanyaan terkait penggunaan website, 
        Anda dapat menghubungi kami melalui kontak berikut:
        </p>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style='font-size:16px; padding-left:50px;'>
        <b>Email:</b> <a href="mailto:alpucaps@gmail.com">alpucaps@gmail.com</a><br>
        <b>Instagram:</b> <a href="https://instagram.com/hnscns" target="_blank">@hnscns</a>
        </div>
        """,
        unsafe_allow_html=True
    )



