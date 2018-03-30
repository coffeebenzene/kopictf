import rsa
import re

(A_public_key, A_private_key) = rsa.newkeys(2048)
(B_public_key, B_private_key) = rsa.newkeys(2048)
(CA_public_key, CA_private_key) = rsa.newkeys(64)

f_A = open("A.txt","w")
f_A.write(str(A_public_key)+"\n")
f_A.write(str(A_private_key))

f_B = open("B.txt","w")
f_B.write(str(B_public_key)+"\n")
f_B.write(str(B_private_key))

f_CA = open("CA.txt","w")
f_CA.write(str(CA_public_key)+"\n")
f_CA.write(str(CA_private_key))


'''
f_r = open("CA.txt","r")

c = f_r.readlines()

for each_line in c:
    if "PublicKey" in each_line:
        pb_list = re.findall('\d+', each_line)

    if "PrivateKey" in each_line:
        pr_list = re.findall('\d+', each_line)

print(pb_list)
print(pr_list)
'''