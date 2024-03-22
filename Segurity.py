import datetime
import os
import jwt
import pytz


class Security():
    secret=os.getenv('secreto')
    tz = pytz.timezone("America/Lima")

    @classmethod
    def generate_token(cls, authenticated_user,perfil):
        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=5),
            'username': authenticated_user,
            'roles': perfil
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]
            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                    roles = payload['roles']
                    if roles:
                        return roles,True
                    return False
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False
        return False