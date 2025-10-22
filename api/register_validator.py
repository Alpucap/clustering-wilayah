import re
from api import get_user_by_username, get_user_by_email

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
def validate_all_fields(username, email, password, confirm_password, db):
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
    
    if not confirm_password:
        errors.append(("confirm_password", "Konfirmasi password wajib diisi"))
    elif password != confirm_password:
        errors.append(("confirm_password", "Password tidak sama"))
        
    return errors
