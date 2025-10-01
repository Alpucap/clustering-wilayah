import streamlit as st
import re
from database import SessionLocal
from api import create_user, get_user_by_email, get_user_by_username

#Method untuk validasi email
def validate_email(email: str) -> bool:
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

#Method untuk validasi password
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

#Method untuk validasi semua field
def validate_all_fields(username, email, password, db):
    """Validate all fields and return list of errors"""
    errors = []
    
    #Username validation
    if not username:
        errors.append(("username", "Username wajib diisi"))
    elif len(username) < 3:
        errors.append(("username", "Username minimal 3 karakter"))
    elif len(username) > 50:
        errors.append(("username", "Username maksimal 50 karakter"))
    elif get_user_by_username(db, username):
        errors.append(("username", "Username sudah dipakai"))
    
    #Email validation
    if not email:
        errors.append(("email", "Email wajib diisi"))
    elif not validate_email(email):
        errors.append(("email", "Format email tidak valid. Contoh: user@domain.com"))
    elif get_user_by_email(db, email):
        errors.append(("email", "Email sudah terdaftar"))
    
    #Password validation
    if not password:
        errors.append(("password", "Password wajib diisi"))
    elif not validate_password(password):
        errors.append(("password", "Password minimal 8 karakter dengan huruf besar, kecil, angka, dan simbol"))
    
    return errors

def show():
    st.markdown(
        "<h1 style='text-align: center; font-weight: bold;'>Register</h1>", 
        unsafe_allow_html=True
    )

    #Validasi
    if 'field_errors' not in st.session_state:
        st.session_state.field_errors = {}

    #Username field
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

    #Email field
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

    #Password field
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

    st.markdown("<small>* Field wajib diisi</small>", unsafe_allow_html=True)

    #Daftar button
    if st.button("Daftar", use_container_width=True):
        db = SessionLocal()
        errors = validate_all_fields(username, email, password, db)

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
    st.markdown(
        """
        <div style="text-align: center; margin-top: 15px; font-size: 16px;">
            Sudah punya akun? 
            <a href="#" style="color: #2563EB; text-decoration: underline; font-weight: 500;"
                onclick="window.location.reload();">
                Login sekarang
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
