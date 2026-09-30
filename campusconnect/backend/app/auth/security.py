import os, base64, json, hashlib, hmac, secrets, time

SECRET_KEY = os.getenv("JWT_SECRET", "dev-only-change-this-campusconnect-secret")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _unb64(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def hash_password(password: str) -> str:
    # Standard-library password hashing; avoids keeping plaintext passwords in the database.
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${_b64(salt)}${_b64(digest)}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        scheme, salt, digest = encoded.split("$", 2)
        if scheme != "scrypt":
            return False
        derived = hashlib.scrypt(password.encode(), salt=_unb64(salt), n=2**14, r=8, p=1)
        return hmac.compare_digest(derived, _unb64(digest))
    except Exception:
        return False


def create_access_token(data: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    payload["iat"] = int(time.time())
    payload["exp"] = int(time.time()) + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    encoded_header = _b64(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = _b64(json.dumps(payload, separators=(",", ":")).encode())
    signing = f"{encoded_header}.{encoded_payload}".encode()
    sig = _b64(hmac.new(SECRET_KEY.encode(), signing, hashlib.sha256).digest())
    return f"{encoded_header}.{encoded_payload}.{sig}"


def decode_token(token: str) -> dict:
    header, payload, signature = token.split(".", 2)
    signing = f"{header}.{payload}".encode()
    expected = _b64(hmac.new(SECRET_KEY.encode(), signing, hashlib.sha256).digest())
    if not hmac.compare_digest(signature, expected):
        raise ValueError("invalid signature")
    data = json.loads(_unb64(payload))
    if int(data.get("exp", 0)) < int(time.time()):
        raise ValueError("expired token")
    return data
