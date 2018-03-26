from socketserver import BaseRequestHandler, ThreadingTCPServer
from socket import *
import random


BUFFSIZE = 1024

class Model:
    def __init__(self):
        self.g_public_prime_base = 5
        self.p_public_prime_modulus = 23
        self.a_ = random.randint(0, 10)
        msg = "Random a_ gen: " + str(self.a_)
        print(msg)
        self.state_list = ["Send g,p,A", "Receive B and Send K", "Empty"]
        self.state = self.state_list[0]



class Handler(BaseRequestHandler):


    def handle(self):
        address,pid = self.client_address
        print('%s connected!'%address)
        md = Model()
        while True:
            # Generate a random num
            if md.state == md.state_list[0]:
                A = pow(md.g_public_prime_base, md.a_) % md.p_public_prime_modulus
                g_p_A = str(md.g_public_prime_base) + "," + str(md.p_public_prime_modulus) + "," + str(A)
                print(g_p_A)
                self.request.send(g_p_A.encode())
                print("g_p_A sent")
                md.state = md.state_list[1]  # wait for B

            if md.state == md.state_list[1]:
                data = self.request.recv(BUFFSIZE)
                if data:
                    B_str = data.decode()
                    msg = "Receive B: "+B_str
                    print(msg)
                    B = int(B_str)
                    md.state = md.state_list[2]
                    K = pow(B,md.a_)%md.p_public_prime_modulus
                    print(K)



if __name__ == '__main__':
    HOST = gethostname()
    PORT = 2334
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)  #参数为监听地址和已建立连接的处理类
    print('listening')
    server.serve_forever()
    print(server)
