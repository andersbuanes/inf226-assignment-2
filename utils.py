from threading import local
from typing import Tuple
from urllib.parse import urlparse, urljoin

import flask
import bcrypt;
from pygments.formatters import HtmlFormatter

tls = local()

def is_safe_url(target):
    ref_url = urlparse(flask.request.host_url)
    test_url = urlparse(urljoin(flask.request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc

def hash_password(password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
    bytes = password.encode('utf-8')
    if not salt:
        salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    
    return (hash, salt)

def check_password_hash(hash: str, inputed_password: str, salt: bytes) -> bool:
    return hash == hash_password(inputed_password, salt)[0]

cssData = HtmlFormatter(nowrap=True).get_style_defs('.highlight')
