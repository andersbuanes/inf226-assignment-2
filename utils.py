from threading import local
from typing import Tuple
from urllib.parse import urlparse, urljoin

import flask
import bcrypt;
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter
from pygments.filters import NameHighlightFilter, KeywordCaseFilter
from pygments import token;

tls = local()

def pygmentize(text):
    if not hasattr(tls, 'formatter'):
        tls.formatter = HtmlFormatter(nowrap = True)
    if not hasattr(tls, 'lexer'):
        tls.lexer = SqlLexer()
        tls.lexer.add_filter(NameHighlightFilter(names=['GLOB'], tokentype=token.Keyword))
        tls.lexer.add_filter(NameHighlightFilter(names=['text'], tokentype=token.Name))
        tls.lexer.add_filter(KeywordCaseFilter(case='upper'))
    return f'<span class="highlight">{highlight(text, tls.lexer, tls.formatter)}</span>'

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
