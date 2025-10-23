import streamlit as st
import base64

#Method untuk mengambil gambar
def get_base64_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

#Method untuk membuat card
def create_card_section(title, items, columns=3, show_title_in_card=True, show_section_title=True):
        if show_section_title:
            st.markdown(
                f"""
                <h2 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:30px;'>
                    {title}
                </h2>
                """,
                unsafe_allow_html=True
            )
        
        #Untuk Manfaat Website
        if items and isinstance(items[0], str):
            cols = st.columns(columns, gap="medium")
            for idx, item in enumerate(items):
                with cols[idx]:
                    st.markdown(
                        f"""
                        <div class="info-card" style="height: 100%; display: flex; align-items: center; justify-content: center;">
                            <p style="margin: 0; line-height: 1.6; text-align: center;">{item}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        #Untuk Indikator dan Metode
        else:
            for i in range(0, len(items), columns):
                cols = st.columns(columns, gap="medium")
                for j in range(columns):
                    if i + j < len(items):
                        with cols[j]:
                            item = items[i + j]
                            if show_title_in_card:
                                st.markdown(
                                    f"""
                                    <div class="info-card">
                                        <h3>{item['title']}</h3>
                                        <p>{item['description']}</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
        
        st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)