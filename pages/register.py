import streamlit as st
from database import SessionLocal
from api.user import create_user
from api.register_validator import validate_all_fields

def show():
    st.markdown(
        "<h1 style='text-align: center; font-weight: bold;'>Create Account</h1>", 
        unsafe_allow_html=True
    )

    #Validasi
    if 'field_errors' not in st.session_state:
        st.session_state.field_errors = {}

    #Username
    username = st.text_input(
        "Username *", 
        placeholder="Masukkan username (3-50 karakter)",
        help="Username harus unik dan antara 3-50 karakter"
    )
    if 'username' in st.session_state.field_errors:
        st.markdown(
            f"<p style='color: red; font-size: 14px; margin-top: -10px;'>{st.session_state.field_errors['username']}</p>", 
            unsafe_allow_html=True
        )

    #Email
    email = st.text_input(
        "Email *", 
        placeholder="contoh@domain.com",
        help="Masukkan alamat email yang valid"
    )
    if 'email' in st.session_state.field_errors:
        st.markdown(
            f"<p style='color: red; font-size: 14px; margin-top: -10px;'>{st.session_state.field_errors['email']}</p>", 
            unsafe_allow_html=True
        )

    #Password
    password = st.text_input(
        "Password *", 
        type="password",
        placeholder="Minimal 8 karakter dengan huruf besar, kecil, angka, dan simbol",
        help="Password harus mengandung huruf besar, kecil, angka, dan simbol"
    )
    if 'password' in st.session_state.field_errors:
        st.markdown(
            f"<p style='color: red; font-size: 14px; margin-top: -10px;'>{st.session_state.field_errors['password']}</p>", 
            unsafe_allow_html=True
        )
    
    #Confirm Password
    confirm_password = st.text_input(
        "Konfirmasi Password *", 
        type="password",
        placeholder="Ulangi Password Diatas",
        help="Isi harus sama dengan password diatas"
    )
    if 'confirm_password' in st.session_state.field_errors:
        st.markdown(
            f"<p style='color: red; font-size: 14px; margin-top: -10px;'>{st.session_state.field_errors['confirm_password']}</p>", 
            unsafe_allow_html=True
        )

    st.markdown("<small>* Field wajib diisi</small>", unsafe_allow_html=True)

    #Daftar button
    if st.button("Daftar", use_container_width=True):
        db = SessionLocal()
        errors = validate_all_fields(username, email, password, confirm_password, db)
        
        if errors:
            st.session_state.field_errors = {field: message for field, message in errors}
            st.rerun()
        else:
            st.session_state.field_errors = {}
            
            user = create_user(db, username, email, password)
            st.success(f"Akun berhasil dibuat untuk {user.username}")

            st.session_state.page = "login"
            st.rerun()

    #Link ke Login
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Sudah Punya Akun? Login sekarang", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
