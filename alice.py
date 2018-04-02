from socketserver import BaseRequestHandler, ThreadingTCPServer
import socket

import rsa

import router_lib
import cert
import dhke

ALICE_CERT = cert.Certificate.load("alice.crt")
with open("alice.pem","rb") as f:
    ALICE_PRI = rsa.PrivateKey.load_pkcs1(f.read())



class Handler(BaseRequestHandler):

    def handle(self):
        sock = router_lib.SocketWrapper(self.request)
        dh_key = dhke.DHKey()
        
        # 1st message A to B
        data = {"p":dh_key.p, "g":dh_key.g, "ga":dh_key.ga}
        signed_json = cert.signed_json(data, ALICE_PRI, ALICE_CERT)
        sock.send(signed_json.encode("utf-8"))
        
        # 2nd message
        pass



if __name__ == '__main__':
    HOST = "localhost"
    PORT = 64127
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)
    print('listening')
    server.serve_forever()
