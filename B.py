from socketserver import BaseRequestHandler, ThreadingTCPServer
from socket import *
import random
import KeyReader
import rsa
import cert
import json
import base64
import hashlib


BUFFSIZE = 4096

class Model:
    def __init__(self):
        self.g_public_prime_base = -1
        self.p_public_prime_modulus = -1
        self.b_ = random.randint(0, 10)
        msg = "Random b_ gen: " + str(self.b_)
        print(msg)

        self.state_list = ["Listen from A and Respond",
                           "Compute K",
                           "Empty"]

        self.state = self.state_list[0]
        self.keypair = KeyReader.get_key("B.txt")
        self.public_key = self.keypair[0]
        self.private_key = self.keypair[1]

        self.state = self.state_list[0]

        self.A = -1
        self.B = -1

        # B_sign = RSA(H(B), B_pri_key)
        self.B_sign = ""

        # B_cert
        self.B_cert = ""

    def create_json(self):
        data_json = {"B": self.B,
                     "B_sign": self.B_sign,
                     "B_cert": self.B_cert,
                     }
        return json.dumps(data_json)


class Handler(BaseRequestHandler):

    def handle(self):
        address,pid = self.client_address
        print('%s connected!'%address)
        md = Model()
        while True:
            if md.state == md.state_list[0]:

                #Extract JSON data
                data_from_A = self.request.recv(BUFFSIZE)
                if data_from_A:
                    json_from_A = data_from_A.decode()
                    dict = json.loads(json_from_A)
                    gpA = dict["p,g,A"]
                    A_sign = dict["A_sign"]
                    A_cert = json.loads(dict["A_cert"])
                    A_pub  = rsa.PublicKey.load_pkcs1(A_cert["rsa_pub"])
                    A_pub_pksc1 = A_cert["rsa_pub"]
                    A_cert_id = A_cert["subject_principal"]
                    CA_sign = A_cert["signature"]

                    # Verify ID to A_signature to CA_signature
                    if A_cert_id == "A":
                        print("ID pass")
                        if cert.validate_rsa(gpA, A_sign, A_pub) == True:
                            print("A_sign pass")
                            if cert.validate_CA_sign(A_pub_pksc1, CA_sign) == True:
                                print("CA_sign pass")

                                # Obtain g p A and load to model class
                                dict_gpA = json.loads(gpA)
                                md.g_public_prime_base = int(dict_gpA["g"])
                                md.p_public_prime_modulus = int(dict_gpA["p"])
                                md.A = int(dict_gpA["A"])

                                # Compute B
                                md.B = pow(md.g_public_prime_base, md.b_) % md.p_public_prime_modulus

                                # B_sign
                                md.B_sign = cert.sign_rsa(str(md.B), md.private_key)

                                # Gen cert
                                md.B_cert = cert.Certificate("B", md.public_key, cert.CA_sign(md.public_key.save_pkcs1().decode("ASCII"))).json()

                                # Create JSON and send to A
                                plain = md.create_json()
                                to_send = plain.encode()
                                self.request.send(to_send)

                                # Jump to next state to compute share K
                                md.state = md.state_list[1]

            if md.state == md.state_list[1]:

                K = pow(md.A, md.b_) % md.p_public_prime_modulus
                msg = "K: " + str(K)
                print(msg)

                # Jump to next state
                md.state = md.state_list[2]



if __name__ == '__main__':
    HOST = gethostname()
    PORT = 2335
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)
    print('listening')
    server.serve_forever()
    print(server)