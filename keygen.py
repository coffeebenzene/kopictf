import rsa
import cert

import time
start = time.time()

A_pub, A_pri = rsa.newkeys(2048)
print("generated A's keys")
B_pub, B_pri = rsa.newkeys(2048)
print("generated B's keys")
ca_p = rsa.prime.getprime(1024)
ca_n = ca_p**2
ca_e = 65537
phi = ca_p*(ca_p-1)
ca_d = rsa.common.inverse(ca_e, phi)
CA_pri = rsa.PrivateKey(ca_n, ca_e, ca_d, ca_p, ca_p-1)
CA_pub = rsa.PublicKey(ca_n, ca_e)
#CA_pub, CA_pri = rsa.newkeys(64)
print("generated CA's keys")

with open("alice.pem","wb") as f:
    f.write(A_pri.save_pkcs1())
alice_cert = cert.Certificate("Alice", A_pub, None)
alice_cert.sign(CA_pri)
alice_cert.save("alice.crt")
print("Written A's keys")

with open("bob.pem","wb") as f:
    f.write(B_pri.save_pkcs1())
bob_cert = cert.Certificate("Bob", B_pub, None)
bob_cert.sign(CA_pri)
bob_cert.save("bob.crt")
print("Written B's keys")

with open("ca.pem","wb") as f:
    f.write(CA_pri.save_pkcs1())
CA_cert = cert.Certificate("Cognitive Accomplice", CA_pub, None)
CA_cert.sign(CA_pri)
CA_cert.save("ca.crt")
print("Written CA's keys")

print("Testing...")
A_cert_test = cert.Certificate.load("alice.crt")
B_cert_test = cert.Certificate.load("bob.crt")
CA_cert_test = cert.Certificate.load("ca.crt")
A_valid = A_cert_test.validate(CA_cert_test.rsa_pub)
print("A valid: {}".format(A_valid))
B_valid = B_cert_test.validate(CA_cert_test.rsa_pub)
print("B valid: {}".format(B_valid))
CA_valid = CA_cert_test.validate(CA_cert_test.rsa_pub)
print("CA valid: {}".format(CA_valid))

print(time.time() - start)