import rsa

import cert
import dhke

### rsa library documentation : https://stuvel.eu/python-rsa-doc/index.html
### Example : Generate a RSA key pair.
public_key, private_key = rsa.newkeys(64) # argument is bit size of key
# keys can be printed.
print(public_key)
print(private_key)



### Example : Save a RSA private key.
with open("example_private.pem","wb") as f:
    f.write(private_key.save_pkcs1())



### Example : load a private key .pem file
with open("example_private.pem","rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())



### Example : Create a certificate
cert_obj = cert.Certificate("My Name", public_key, None)
# Certificate can be printed (note attribute names)
print(cert_obj)



### Example : Sign a certificate
cert_obj.sign(private_key)



### Example : Validate a certificate
print(cert_obj.validate(public_key))



### Example : Save a certificate to file
cert_obj.save("example.crt")



### Example : load a certificate
cert_obj = cert.Certificate.load("example.crt")



### Example : Adding signature to dict of data.
data = {"field1":123, "field2":"Only int or str values allowed"}
signed_data = cert.create_signed_dict(data, private_key, cert_obj)
print(signed_data)



### Example : Validating content with signature of signed data. ASSUMES cert is valid.
isvalid = cert.validate_signed_dict(signed_data)
print(isvalid)
signed_data["newfield"] = 1  # Modify data
isinvalid = cert.validate_signed_dict(signed_data)
print(isinvalid)



### Example Inverse modulo
# Given x and n, a = x^-1 mod n AKA a*x = 1 mod n
x = 5
n = 3
a = cert.inverse_mod(x, n)  # 2*5 mod 3 = 1
print(a) # 2



### Example : Diffie-Hellman Key Exchange
# Step 1 : A generates key
a_dhkey = dhke.DHKey()
print(a_dhkey.p)    # p value of DHKE protocol. (prime modulus)
print(a_dhkey.g)    # g value of DHKE protocol. (generator)
print(a_dhkey.a)    # A's diffie-Hellman 'private' key, a (randomised value)
print(a_dhkey.ga)   # g^a % p
print(a_dhkey.gab)  # shared key : g^ab % p = None (not computed yet)

# Step 2 : B generates key from A's g, p.
b_dhkey = dhke.DHKey(a_dhkey.p, a_dhkey.g)
print(b_dhkey.a)  # B's diffie-Hellman 'private' key, b (randomised value)
                  # Note: The 'private' key is always referenced by attribute a.

# Step 3 : B computes g^ab %p
b_dhkey.compute_shared(a_dhkey.ga)
print(b_dhkey.gab)

# Step 4 : A computes g^ab %p
a_dhkey.compute_shared(b_dhkey.ga)
print(a_dhkey.gab)



### Example : Diffie-Hellman based AES256 Encryption (A to B)
ciphertext, iv = dhke.aes256_dhke_encrypt(a_dhkey, "Hello! This is a test message") # A's key
# send ciphertext to B here...
plaintext = dhke.aes256_dhke_decrypt(b_dhkey, ciphertext, iv) # B's key
print(plaintext)