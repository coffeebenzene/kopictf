import rsa
import re

(A_public_key, A_private_key) = rsa.newkeys(2048)
(B_public_key, B_private_key) = rsa.newkeys(2048)
(CA_public_key, CA_private_key) = rsa.newkeys(256)

f_A = open("A.txt","w")
f_A.write(str(A_public_key)+"\n")
f_A.write(str(A_private_key))

f_B = open("B.txt","w")
f_B.write(str(B_public_key)+"\n")
f_B.write(str(B_private_key))

f_CA = open("CA.txt","w")
f_CA.write(str(CA_public_key)+"\n")
f_CA.write(str(CA_private_key))


