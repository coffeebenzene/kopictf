import KeyReader
import rsa



def gen_cert(id, public_key):
    keypair = KeyReader.get_key("CA.txt")
    CA_public_key = keypair[0]
    CA_private_key = keypair[1]
    id_encode = id.encode()
    plain = str(public_key).encode()
    signature_CA = rsa.sign(plain, CA_private_key, 'MD5')

    cert_msg = id_encode + plain + signature_CA
    return cert_msg

