import base64
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA

from ossManager import appserver


def verrify(auth_str, authorization_base64, pub_key):
    """
    校验签名是否正确（MD5 + RAS）
    :param auth_str: 文本信息
    :param authorization_base64: 签名信息
    :param pub_key: 公钥
    :return: 若签名验证正确返回 True 否则返回 False
    """
    pub_key_load = RSA.importKey(pub_key)
    auth_md5 = MD5.new(auth_str.encode())
    result = False
    try:
        result = PKCS1_v1_5.new(pub_key_load).verify(auth_md5, base64.b64decode(authorization_base64.encode()))
    except Exception as e:
        print(e)
        result = False
    return result


def get_http_request_unquote(url):
    return urllib.request.unquote(url)


def get_pub_key(pub_key_url_base64):
    """ 抽取出 public key 公钥 """
    pub_key_url = base64.b64decode(pub_key_url_base64.encode())
    url_reader = urllib.request.urlopen(pub_key_url.decode())
    pub_key = url_reader.read()
    return pub_key


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """处理 POST 请求"""
        return appserver.do_POST(self)

    def do_GET(self):
        """处理 GET 请求"""
        appserver.do_GET(self)


class MyHTTPServer(HTTPServer):
    def __init__(self, host, port):
        print("run app server by python3!")
        HTTPServer.__init__(self, (host, port), MyHTTPRequestHandler)
