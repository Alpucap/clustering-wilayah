import streamlit as st
from database import SessionLocal
from api.user import get_user_by_email
from api.login_validator import validate_login_fields

def show(cookies):
    st.markdown("<h1 style='text-align:center;font-weight:bold;'>Selamat Datang Kembali</h1>", unsafe_allow_html=True)

    if "user_id" in st.session_state:
        st.info(f"Anda sudah login sebagai {st.session_state['username']}")
        return

    if 'login_field_errors' not in st.session_state:
        st.session_state.login_field_errors = {}

    email = st.text_input("Email *", placeholder="Masukkan email Anda")
    if 'email' in st.session_state.login_field_errors:
        st.markdown(f"<p style='color:red;font-size:14px;margin-top:-10px;'>{st.session_state.login_field_errors['email']}</p>", unsafe_allow_html=True)

    password = st.text_input("Password *", type="password", placeholder="Masukkan password Anda")
    if 'password' in st.session_state.login_field_errors:
        st.markdown(f"<p style='color:red;font-size:14px;margin-top:-10px;'>{st.session_state.login_field_errors['password']}</p>", unsafe_allow_html=True)

    st.markdown("<small>* Field wajib diisi</small>", unsafe_allow_html=True)

    if st.button("Login", use_container_width=True):
        db = SessionLocal()
        errors = validate_login_fields(email, password, db)

        if errors:
            st.session_state.login_field_errors = {field: message for field, message in errors}
            st.rerun()
        else:
            st.session_state.login_field_errors = {}

            user = get_user_by_email(db, email)
            st.session_state["user_id"] = str(user.user_id)
            st.session_state["username"] = user.username

            cookies["user_id"] = str(user.user_id)
            cookies["username"] = user.username
            cookies.save()

            st.success(f"Selamat datang, {user.username}!")
            st.session_state.page = "beranda"
            st.rerun()
            
    st.markdown("---")
    
    #Link ke register
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Belum Punya Akun? Daftar sekarang", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
