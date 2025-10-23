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
        <p style='text-align: center; font-size:16px; padding-left:50px; padding-right:50px;'>
        Jika membutuhkan informasi lebih lanjut atau memiliki pertanyaan terkait penggunaan website, 
        Anda dapat menghubungi kami melalui kontak berikut:
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .contact-icon {
            transition: transform 0.2s ease-in-out;
            display: inline-block;
        }
        .contact-icon:hover {
            transform: scale(1.15);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='display: flex; justify-content: center; gap: 40px; padding: 20px;'>
            <a href="mailto:alpucaps@gmail.com" target="_blank" style='text-decoration: none;'>
                <div style='text-align: center;' class="contact-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" 
                        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" 
                        stroke-linecap="round" stroke-linejoin="round" style='color: #fafafa;'>
                        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                        <polyline points="22,6 12,13 2,6"></polyline>
                    </svg>
                    <p style='margin-top: 8px; color: #f5f5f5; font-size: 14px;'>Email</p>
                </div>
            </a>
            <a href="https://instagram.com/hnscns" target="_blank" style='text-decoration: none;'>
                <div style='text-align: center;' class="contact-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" 
                        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" 
                        stroke-linecap="round" stroke-linejoin="round" style='color: #fafafa;'>
                        <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                        <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                        <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                    </svg>
                    <p style='margin-top: 8px; color: #f5f5f5; font-size: 14px;'>Instagram</p>
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
