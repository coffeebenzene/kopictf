from socketserver import BaseRequestHandler, ThreadingTCPServer
from socket import *
import random


BUFFSIZE = 1024

class Model:
    def __init__(self):
        self.g_public_prime_base = -1
        self.p_public_prime_modulus = -1
        self.b_ = random.randint(0, 10)
        msg = "Random b_ gen: " + str(self.b_)
        print(msg)
        self.state_list = ["Send g,p,A", "Receive A and Send B", "Empty"]
        self.state = self.state_list[0]



class Handler(BaseRequestHandler):

    def handle(self):
        address,pid = self.client_address
        print('%s connected!'%address)
        md = Model()
        while True:
            if md.state == md.state_list[0]:
                data = self.request.recv(BUFFSIZE)
                if data:
                    str_rcv = data.decode()
                    print(str_rcv)
                    g_p_A_list = list(map(int, str_rcv.split(',')))
                    md.state = md.state_list[1]

            if md.state == md.state_list[1]:

                md.g_public_prime_base = g_p_A_list[0]
                md.p_public_prime_modulus = g_p_A_list[1]

                A = g_p_A_list[2]
                msg = "Receive A: " + str(A)
                print(msg)

                B = pow(md.g_public_prime_base, md.b_) % md.p_public_prime_modulus

                msg = "B=pow("+str(md.g_public_prime_base)+","+str(md.b_)+")mod"+str(md.p_public_prime_modulus)
                print(msg)

                B_str = str(B)
                self.request.send(B_str.encode())
                print("B sent: " + B_str)
                md.state = md.state_list[2]
                K = pow(A, md.b_) % md.p_public_prime_modulus
                msg = "K: " + str(K)
                print(msg)



if __name__ == '__main__':
    HOST = gethostname()
    PORT = 2335
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)
    print('listening')
    server.serve_forever()
    print(server)