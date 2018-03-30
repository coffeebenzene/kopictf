from socket import *

HOST = gethostname()
B_PORT = 2335
A_PORT = 2334
BUFFSIZE = 1024

B_ADDR = (HOST, B_PORT)
A_ADDR = (HOST, A_PORT)

# Connection from Router to B
tcp_R_B = socket(AF_INET, SOCK_STREAM)
tcp_R_B.connect(B_ADDR)

# Connection from Router to A
tcp_R_A = socket(AF_INET, SOCK_STREAM)
tcp_R_A.connect(A_ADDR)

while True:
    #TODO:
    data_from_A = tcp_R_A.recv(BUFFSIZE) #Wait
    if data_from_A:
        print("Received from A")
        tcp_R_B.send(data_from_A)
    if not data_from_A:
        break
    data_from_B = tcp_R_B.recv(BUFFSIZE) #Wait
    if data_from_B:
        print("Received from B")
        tcp_R_A.send(data_from_B)
    if not data_from_B:
        break

print("Client off")
tcp_R_A.close()
tcp_R_B.close()