import streamlit as st

def render_sidebar(cookies=None):
    def set_page(page_name):
        st.session_state.page = page_name
        if cookies is not None:
            cookies["page"] = page_name
            cookies.save()
        st.rerun()  # ⬅️ langsung rerun biar pindah sekali klik

    if st.sidebar.button("Beranda", use_container_width=True):
        set_page("beranda")

    if st.sidebar.button("Clustering Wilayah", use_container_width=True):
        set_page("clustering")

    if st.sidebar.button("Petunjuk Penggunaan", use_container_width=True):
        set_page("petunjuk")

    if st.sidebar.button("Tentang", use_container_width=True):
        set_page("tentang")

    st.sidebar.markdown("---")

    if "user_id" not in st.session_state:
        if st.sidebar.button("Login", use_container_width=True):
            set_page("login")
        if st.sidebar.button("Register", use_container_width=True):
            set_page("register")
    else:
        if st.sidebar.button("Profile", use_container_width=True):
            set_page("profile")
