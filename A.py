from socketserver import BaseRequestHandler, ThreadingTCPServer
from socket import *
import random
import KeyReader
import rsa
import cert
import json

BUFFSIZE = 4096

class Model:
    def __init__(self):
        self.g_public_prime_base = 5
        self.p_public_prime_modulus = 23
        self.a_ = random.randint(0, 10)
        msg = "Random a_ gen: " + str(self.a_)
        print(msg)

        self.state_list = ["Send g, p, A || A_sign || CA_cert (id + Pub_key + CA_sign)",
                           "Receive B and Compute K",
                           "Empty"]

        self.state = self.state_list[0]
        self.keypair = KeyReader.get_key("A.txt")
        self.public_key = self.keypair[0]
        self.private_key = self.keypair[1]

        # Compute A=g^a%p and formulate str = g,p,g^a%p
        self.A = pow(self.g_public_prime_base, self.a_) % self.p_public_prime_modulus
        self.B = -1
        self.g_p_A = json.dumps({"g": self.g_public_prime_base,
                                 "p": self.p_public_prime_modulus,
                                 "A": self.A,
                                 })

        # A_sign = RSA(H(p,g,A), A_pri_key)
        self.A_sign = cert.sign_rsa(self.g_p_A, self.private_key)

        # Gen_cert
        self.A_cert = cert.Certificate("A", self.public_key, cert.CA_sign(self.public_key.save_pkcs1().decode("ASCII"))).json()

    def create_json(self):
        data_json = {"p,g,A": self.g_p_A,
                      "A_sign": self.A_sign,
                      "A_cert": self.A_cert,
                      }
        return json.dumps(data_json)


class Handler(BaseRequestHandler):

    def handle(self):
        address,pid = self.client_address
        print('%s connected!'%address)
        md = Model()
        while True:
            # Generate a random num
            if md.state == md.state_list[0]:

                # Send json to B (g,p,A || A_sign || A_Cert)
                plain = md.create_json()
                to_send = plain.encode()
                self.request.send(to_send)

                md.state = md.state_list[1]  # wait for B

            if md.state == md.state_list[1]:
                data_from_B = self.request.recv(BUFFSIZE)
                if data_from_B:
                    json_from_B = data_from_B.decode()
                    dict = json.loads(json_from_B)
                    B = dict["B"]
                    B_sign = dict["B_sign"]
                    B_cert = json.loads(dict["B_cert"])
                    B_pub  = rsa.PublicKey.load_pkcs1(B_cert["rsa_pub"])
                    B_pub_pksc1 = B_cert["rsa_pub"]
                    B_cert_id = B_cert["subject_principal"]
                    CA_sign = B_cert["signature"]

                    # Verify ID to B_signature to CA_signature
                    if B_cert_id == "B":
                        print("ID pass")
                        if cert.validate_rsa(str(B), B_sign, B_pub) == True:
                            print("A_sign pass")
                            if cert.validate_CA_sign(B_pub_pksc1, CA_sign) == True:
                                print("CA_sign pass")

                                # Obtain g p A and load to model class
                                md.B = int(B)

                                # Compute K
                                K = pow(md.B, md.a_) % md.p_public_prime_modulus
                                msg = "K: " + str(K)
                                print(msg)

                                # Jump to next state
                                md.state = md.state_list[2]





if __name__ == '__main__':
    HOST = gethostname()
    PORT = 2334
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)
    print('listening')
    server.serve_forever()
    print(server)
