import streamlit as st
from database import SessionLocal
from api import get_user_by_id, get_user_by_username
from sqlalchemy.orm import Session
from datetime import datetime

def show(cookies):
    
    #Validasi
    if "user_id" not in st.session_state:
        st.warning("Anda harus login terlebih dahulu.")
        return

    db: Session = SessionLocal()
    user = get_user_by_id(db, st.session_state["user_id"])

    #Header Info
    st.markdown(
        f"""
        <div style="text-align:center; margin-top:40px; margin-bottom:40px;">
            <p style="margin-bottom:4px; font-size:48px; font-weight:bold;">{user.username}</p>
            <p style="font-size:18px; color:#ccc; margin:0;">{user.email}</p>
            <p style="font-size:15px; color:#aaa; margin-top:16px;">
                Dibuat pada: {datetime.strftime(user.created_at, "%d %b %Y")}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()

    #Ganti Username
    st.subheader("Ganti Username")
    new_username = st.text_input("Username baru", placeholder="Masukkan username baru")

    if st.button("Simpan", use_container_width=True):
        if not new_username:
            st.error("Username baru tidak boleh kosong.")
        elif get_user_by_username(db, new_username):
            st.error("Username sudah dipakai.")
        else:
            user.username = new_username
            db.commit()
            st.success("Username berhasil diperbarui.")

            st.session_state["username"] = new_username
            cookies["username"] = new_username
            cookies.save()
            st.rerun()

    st.divider()

    #Logout dan Delete Account
    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            cookies["user_id"] = ""
            cookies["username"] = ""
            cookies.save()

            st.success("Anda telah logout.")
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("Hapus Akun", use_container_width=True):
            st.session_state.show_delete_confirmation = True

    #Delete Confirmation
    if st.session_state.get('show_delete_confirmation', False):
        st.markdown("<br>", unsafe_allow_html=True)
        st.error("**Apakah Anda yakin ingin menghapus akun ini?**")
        
        confirm = st.checkbox("Saya yakin dan memahami bahwa tindakan ini tidak dapat dibatalkan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Batal", use_container_width=True):
                st.session_state.show_delete_confirmation = False
                st.rerun()

        with col2:
            if st.button("Ya, Hapus", type="primary", disabled=not confirm, use_container_width=True):
                db.delete(user)
                db.commit()
                st.session_state.clear()

                cookies["user_id"] = ""
                cookies["username"] = ""
                cookies.save()

                st.session_state.show_delete_confirmation = False
                st.success("Akun berhasil dihapus.")
                st.session_state.page = "register"
                st.rerun()

    if 'show_delete_confirmation' not in st.session_state:
        st.session_state.show_delete_confirmation = False