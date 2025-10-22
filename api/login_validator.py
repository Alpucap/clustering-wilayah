from api import get_user_by_email, verify_password

#Method untuk validasi login
def validate_login_fields(email, password, db):
    """Validate login fields and return list of errors"""
    errors = []
    if not email:
        errors.append(("email", "Email wajib diisi"))
    else:
        user = get_user_by_email(db, email)
        if not user:
            errors.append(("email", "Email tidak terdaftar"))
        elif password and not verify_password(password, user.password):
            errors.append(("password", "Password salah"))
    if not password:
        errors.append(("password", "Password wajib diisi"))
    return errors
