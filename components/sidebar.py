import streamlit as st

def render_sidebar(cookies=None):
    def set_page(page_name):
        st.session_state.page = page_name
        if cookies is not None:
            cookies["page"] = page_name
            cookies.save()
        st.rerun()

    if st.sidebar.button("Beranda", width= 'stretch'):
        set_page("beranda")

    if st.sidebar.button("Clustering Wilayah", width= 'stretch'):
        set_page("clustering_wilayah")
    
    if st.sidebar.button("Hasil Clustering Wilayah", width= 'stretch'):
        set_page("hasil_clustering")
    
    if st.sidebar.button("Riwayat Clustering", width= 'stretch'): 
        set_page("riwayat")

    if st.sidebar.button("Petunjuk Penggunaan", width= 'stretch'):
        set_page("petunjuk_penggunaan_website")

    if st.sidebar.button("Tentang", width= 'stretch'):
        set_page("tentang")

    st.sidebar.markdown("---")

    if "user_id" not in st.session_state:
        if st.sidebar.button("Login", width= 'stretch'):
            set_page("login")
        if st.sidebar.button("Register", width= 'stretch'):
            set_page("register")
    else:
        if st.sidebar.button("Profile", width= 'stretch'):
            set_page("profile")
