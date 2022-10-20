from msilib.schema import AppId
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jwt.utils import get_int_from_datetime
from .constants import APP_ID
load_dotenv()

from jwt import jwk_from_pem, JWT


class GetJwtToken:

    def __init__(self,pempath):
        self.pempath=pempath

    def getToken(self):
        with open(self.pempath, 'rb') as fh:
            private_key = jwk_from_pem(fh.read())

        payload = {
            'iat':get_int_from_datetime(datetime.now(timezone.utc)),
            'exp': get_int_from_datetime(
                datetime.now(timezone.utc) + timedelta(minutes=1)),
            'iss': APP_ID

        }

        jwt_token = JWT().encode(payload,private_key,alg='RS256')
        
        return jwt_token
