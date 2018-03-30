import rsa
import cert

A_pub, A_pri = rsa.newkeys(2048)
B_pub, B_pri = rsa.newkeys(2048)
CA_pub, CA_pri = rsa.newkeys(64)

with open("alice.pem","wb") as f:
    f.write(A_pri.save_pkcs1())
alice_cert = cert.Certificate("Alice", A_pub, None)
alice_cert.sign(CA_pri)
alice_cert.save("alice.crt")

with open("bob.pem","wb") as f:
    f.write(B_pri.save_pkcs1())
bob_cert = cert.Certificate("Bob", B_pub, None)
bob_cert.sign(CA_pri)
bob_cert.save("bob.crt")

CA_cert = cert.Certificate("Certificate Authority", CA_pub, None)
CA_cert.sign(CA_pri)
CA_cert.save("CA.crt")
# CA private key is not saved. Go factor yourself.