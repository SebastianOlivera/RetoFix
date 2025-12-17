import bcrypt

def get_password_hash(password: str) -> str:
    """Hash de contrasenas utilizando bcrypt."""
    if not password:
        raise ValueError("password requerido para generar hash")
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Compara una contrasena en texto plano con su hash almacenado."""
    if not plain_password or not password_hash:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), password_hash.encode("utf-8")
        )
    except ValueError:
        return False
