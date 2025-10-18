import streamlit as st
from components.sidebar import render_sidebar

import pages.beranda as beranda
import pages.clustering_wilayah as clustering_wilayah
import pages.hasil_clustering as hasil_clustering
import pages.login as login
import pages.register as register
import pages.profile as profile
import pages.petunjuk_penggunaan_website as petunjuk_penggunaan_website
import pages.tentang as tentang
import pages.riwayat as riwayat


from database import SessionLocal
from api import get_user_by_id
from streamlit_cookies_manager import EncryptedCookieManager


def page_loader():
    st.markdown(
        """
        <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4da6ff;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        </style>

        <div style="text-align:center; padding:60px;">
            <div class="spinner"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.set_page_config(page_title="Clustering Wilayah di Indonesia", layout="wide")

#Setup cookies manager
secret = st.secrets["COOKIE_PASSWORD"]
cookies = EncryptedCookieManager(prefix="clustering_app_", password=secret)
if not cookies.ready():
    st.stop()

#Restore dari cookies
if "user_id" not in st.session_state:
    user_id = cookies.get("user_id")
    username = cookies.get("username")
    if user_id and username:
        st.session_state["user_id"] = user_id
        st.session_state["username"] = username

#Validasi user_id
if "user_id" in st.session_state:
    db = SessionLocal()
    user = get_user_by_id(db, st.session_state["user_id"])
    if not user:
        st.session_state.clear()
        cookies["user_id"] = ""
        cookies["username"] = ""
        cookies["page"] = ""
        cookies.save()

#Inisialisasi halaman default
if "page" not in st.session_state:
    last_page = cookies.get("page")
    if last_page:
        st.session_state.page = last_page
    else:
        st.session_state.page = "login" if "user_id" not in st.session_state else "beranda"

if "last_page" not in st.session_state:
    st.session_state.last_page = st.session_state.page
    
#Matikan sidebar bawaan
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

#Sidebar custom
render_sidebar(cookies)

#Routing manual
page = st.session_state.page

if page != st.session_state.last_page:
    page_loader()
    st.session_state.last_page = page
    st.rerun()
    
if page == "beranda":
    beranda.show()
elif page == "clustering_wilayah":
    clustering_wilayah.show()
elif page == "hasil_clustering":
    hasil_clustering.show()
elif page == "login":
    login.show(cookies)
elif page == "register":
    register.show()
elif page == "profile":
    profile.show(cookies)
elif page == "petunjuk_penggunaan_website":
    petunjuk_penggunaan_website.show()
elif page == "tentang":
    tentang.show()
elif page == "riwayat":
    riwayat.show(cookies)
