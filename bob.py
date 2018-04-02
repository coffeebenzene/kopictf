from socketserver import BaseRequestHandler, ThreadingTCPServer
import socket
import json
import time

import rsa

import router_lib
import cert
import dhke

CA_CERT = cert.Certificate.load("ca.crt")
BOB_CERT = cert.Certificate.load("bob.crt")
with open("bob.pem","rb") as f:
    BOB_PRI = rsa.PrivateKey.load_pkcs1(f.read())



class Handler(BaseRequestHandler):

    def handle(self):
        sock = router_lib.SocketWrapper(self.request)
        try:
            # Receive 1st message A to B: p, g, ga
            signed_json = sock.recv()
            signed_data = json.loads(signed_json)
            
            alice_cert = cert.Certificate(**signed_data["cert"])
            if not alice_cert.validate(CA_CERT.rsa_pub):
                raise Exception("Certificate attached has an invalid signature!")
            if not alice_cert.subject_principal == "Alice":
                raise Exception("Certificate attached doesn't belong to Alice!")
            
            dh_key = dhke.DHKey(p=signed_data["p"], g=signed_data["g"])
            dh_key.compute_shared(signed_data["ga"])
            
            # Send 2nd message B to A: gb
            data = {"gb":dh_key.ga}
            signed_data = cert.create_signed_dict(data, BOB_PRI, BOB_CERT)
            signed_json = json.dumps(signed_data, sort_keys=True)
            sock.send(signed_json.encode("utf-8"))
            
            # Receive 3rd message A to B: request for image ####
            json_data = sock.recv()
            data = json.loads(json_data)
            req = dhke.aes256_dhke_decrypt(dh_key, data["request"], data["iv"])
            req_start = "can i please have image#"
            if not req.lower().startswith(req_start):
                raise Exception("Sorry, I don't like your request. :(")
            req_id = req[len(req_start):]
            req_id = int(req_id)
            
            # Send 4th message B to A: reply for image ####
            
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
    PORT = 37590
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)
    print('listening')
    server.serve_forever()
