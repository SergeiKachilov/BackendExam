import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import bcrypt


class AuthHandler:
    # настройки для хеширования пароля
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # Секретный ключ, на его основе генерируется JWT токен
    secret = "ljQzOgw0XgEYMcNzHgBuFf8lDsFo6Fd2AqKYELSxcwS"

    # функция получения хеша из пароля
    def get_password_hash(self, password):
        #    return self.pwd_context.hash(password)
        return bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())

    # сверка пароля и хеша
    def verify_password(self, input_pass, hash_pass):
        #    return self.pwd_context.verify(input_pass, hash_pass)
        return bcrypt.checkpw(input_pass.encode(), hash_pass)

    # создание JWT токена, с временем жизни 30 минут
    def encode_token(self, id, role):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
            "sub": id,
            "rol": role,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")
    
    def encode_refresh_token(self, id):
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=3),
            "iat": datetime.utcnow(),
            "sub": id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    # декодирование JWT токена
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            # return {"username": payload["sub"], "role": payload["rol"]}
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Просрочено")
        except jwt.InvalidTokenError as e:
            raise HTTPException(401, "Плохой токен")

    # мидлваре для защиты маршрутов
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
