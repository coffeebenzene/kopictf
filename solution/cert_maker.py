import cert
import rsa

ca_cert = cert.Certificate.load("ca.crt")
n = ca_cert.rsa_pub.n
e = ca_cert.rsa_pub.e

print(n)
print("Factorise n using https://www.alpertron.com.ar/ECM.HTM")
p = int(input("ca p:"))
q = int(input("ca q:"))

if p == q: # perfect square, totient is actually p*(p-1) so make q=p+1
    q = (p+1)

totient = (p-1) * (q-1)
d = cert.inverse_mod(e, totient)

ca_pri = rsa.PrivateKey(n, e, d, p, q)

# Make fake a and b certs.
m_pub, m_pri = rsa.newkeys(64) # small size 64bit.

with open("man.pem","wb") as f:
    f.write(m_pri.save_pkcs1())

alice_cert = cert.Certificate("Alice", m_pub, None)
alice_cert.sign(ca_pri)
alice_cert.save("alice2.crt")

bob_cert = cert.Certificate("Bob", m_pub, None)
bob_cert.sign(ca_pri)
bob_cert.save("bob2.crt")