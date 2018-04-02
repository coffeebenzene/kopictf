from socketserver import BaseRequestHandler, ThreadingTCPServer
import socket

import rsa

import router_lib
import cert
import dhke

BOB_CERT = cert.Certificate.load("bob.crt")
with open("bob.pem","rb") as f:
    BOB_PRI = rsa.PrivateKey.load_pkcs1(f.read())



class Handler(BaseRequestHandler):

    def handle(self):
        sock = router_lib.SocketWrapper(self.request)
        
        # Receive 1st message A to B
        signed_json = sock.recv()
        signed_json = cert.read_signed_json(signed_json)
        
        print(signed_json)
        pass



if __name__ == '__main__':
    HOST = "localhost"
    PORT = 37590
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)
    print('listening')
    server.serve_forever()
