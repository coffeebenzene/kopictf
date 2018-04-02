from socketserver import BaseRequestHandler, ThreadingTCPServer
import socket
import json
import random
import time

import rsa

import router_lib
import cert
import dhke

CA_CERT = cert.Certificate.load("ca.crt")
ALICE_CERT = cert.Certificate.load("alice.crt")
with open("alice.pem","rb") as f:
    ALICE_PRI = rsa.PrivateKey.load_pkcs1(f.read())



class Handler(BaseRequestHandler):

    def handle(self):
        sock = router_lib.SocketWrapper(self.request)
        dh_key = dhke.DHKey()
        
        try:
            # Send 1st message A to B: p, g, ga
            data = {"p":dh_key.p, "g":dh_key.g, "ga":dh_key.ga}
            signed_data = cert.create_signed_dict(data, ALICE_PRI, ALICE_CERT)
            signed_json = json.dumps(signed_data, sort_keys=True)
            sock.send(signed_json.encode("utf-8"))
            
            # Receive 2nd message B to A: gb
            signed_json = sock.recv()
            signed_data = json.loads(signed_json)
            
            bob_cert = cert.Certificate(**signed_data["cert"])
            if not bob_cert.validate(CA_CERT.rsa_pub):
                raise Exception("Certificate attached has an invalid signature!")
            if not bob_cert.subject_principal == "Bob":
                raise Exception("Certificate attached doesn't belong to Bob!")
            
            dh_key.compute_shared(signed_data["gb"])
            
            # Send 3rd message A to B: request for image ####
            req_id = random.randint(0,9998)
            if req_id >= 7258: # Never send 7258, offset numbers
                req_id += 1
            req = "Can I please have image#{:04}".format(req_id)
            ciphertext_req, iv = dhke.aes256_dhke_encrypt(dh_key, req)
            data = {"request":ciphertext_req, "iv":iv}
            json_data = json.dumps(data, sort_keys=True)
            sock.send(json_data.encode("utf-8"))
            
            # Receive 4th message B to A: reply for image ####
            
            print(req_id)
        except Exception as e:
            error = str(e)
            error = json.dumps({"error":error}).encode("utf-8")
            sock.send(error)
        end = json.dumps({"end":1}).encode("utf-8")
        sock.send(end)
        time.sleep(10) # Sleep for awhile so end signal can be seen.



if __name__ == '__main__':
    HOST = "localhost"
    PORT = 64127
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)
    print('listening')
    server.serve_forever()
