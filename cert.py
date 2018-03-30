import json
import base64
<<<<<<< HEAD
import KeyReader
import rsa
# import present
import hashlib


=======

import rsa
#import present
import hashlib

>>>>>>> Kopi_branch
class Certificate():
    def __init__(self, subject_principal, rsa_pub, signature):
        if isinstance(rsa_pub, str) or isinstance(rsa_pub, bytes):
            rsa_pub = rsa.PublicKey.load_pkcs1(rsa_pub)
        if not isinstance(rsa_pub, rsa.PublicKey):
            raise Exception("Invalid rsa_pub")
<<<<<<< HEAD

        self.subject_principal = subject_principal
        self.rsa_pub = rsa_pub
        self.signature = signature

    def __repr__(self):
        template = ('Certificate(\n'
                    '  subject_principal={},\n'
                    '  rsa_pub={},\n'
                    '  signature={}\n)')
        str_self = template.format(repr(self.subject_principal),
                                   repr(self.rsa_pub),
                                   repr(self.signature),
                                   )
        return str_self

=======
        
        self.subject_principal = subject_principal
        self.rsa_pub = rsa_pub
        self.signature = signature
    
    def __repr__(self):
        template = ('Certificate(\n'
                   '  subject_principal={},\n'
                   '  rsa_pub={},\n'
                   '  signature={}\n)')
        str_self = template.format(repr(self.subject_principal),
                                   repr(self.rsa_pub),
                                   repr(self.signature),
                                  )
        return str_self
    
>>>>>>> Kopi_branch
    def json(self):
        cert_json = {"subject_principal": self.subject_principal,
                     "rsa_pub": self.rsa_pub.save_pkcs1().decode("ASCII"),
                     "signature": self.signature,
<<<<<<< HEAD
                     }
        return json.dumps(cert_json)

    def as_msg(self):
        return self.subject_principal + "|" + self.rsa_pub.save_pkcs1().decode("ASCII")

=======
                    }
        return json.dumps(cert_json)
    
    def as_msg(self):
        return self.subject_principal + "|" + self.rsa_pub.save_pkcs1().decode("ASCII")
    
>>>>>>> Kopi_branch
    def sign(self, CA_pri):
        """ Signs certificate. Will reset signature field. """
        msg = self.as_msg()
        self.signature = sign_rsa(msg, CA_pri)
        return self.signature
<<<<<<< HEAD

    def validate(self, CA_pub):
        msg = self.as_msg()
        return validate_rsa(msg, self.signature, CA_pub)


=======
    
    def validate(self, CA_pub):
        msg = self.as_msg()
        return validate_rsa(msg, self.signature, CA_pub)
    
>>>>>>> Kopi_branch
    @classmethod
    def load(cls, filename):
        with open(filename) as f:
            cert_json = json.load(f)
        return cls(**cert_json)
<<<<<<< HEAD

=======
    
>>>>>>> Kopi_branch
    def save(self, filename):
        cert_json = {"subject_principal": self.subject_principal,
                     "rsa_pub": self.rsa_pub.save_pkcs1().decode("ASCII"),
                     "signature": self.signature,
<<<<<<< HEAD
                     }
        with open(filename, "w") as f:
            json.dump(cert_json, f)



# sign_hash function should convert str to int.
hash_length = 64 // 8
sha64 = lambda msg : int.from_bytes(hashlib.sha256(msg.encode("UTF-8")).digest()[:hash_length], "big") # 64bits of SHA256 as int. !!Use sha256 for testing.!!



=======
                    }
        with open(filename,"w") as f:
            json.dump(cert_json, f)


# sign_hash function should convert str to int.
sha64 = lambda msg : int.from_bytes(hashlib.sha256(msg.encode("UTF-8")).digest()[:hash_length], "big") # 64bits of SHA256 as int. !!Use sha256 for testing.!!

>>>>>>> Kopi_branch
def sign_rsa(message, rsa_pri, sign_hash=sha64):
    """message : str
       rsa_pri : rsa.PrivateKey
       outputs: signature (str)
    """
    h = sign_hash(message)
    signature = rsa.core.encrypt_int(h, rsa_pri.d, rsa_pri.n)
    signature = signature.to_bytes(rsa_pri.n.bit_length(), "big")
    signature = base64.b64encode(signature)
    signature = signature.decode("ASCII")
    return signature

<<<<<<< HEAD

def validate_rsa(message, signature, rsa_pub, sign_hash=sha64):
    """message : str
       signature : b64encoded bytes
=======
def validate_rsa(message, signature, rsa_pub, sign_hash=sha64):
    """message : str
       signature : b64encoded str
>>>>>>> Kopi_branch
       rsa_pri : rsa.PublicKey
       outputs: boolean (True if valid)
    """
    h = sign_hash(message)
    signature = signature.encode("ASCII")
    signature = base64.b64decode(signature)
    signature = int.from_bytes(signature, "big")
    h2 = rsa.core.decrypt_int(signature, rsa_pub.e, rsa_pub.n)
<<<<<<< HEAD
    return h == h2

class key_model:
    def __init__(self):
        self.keypair = KeyReader.get_key("CA.txt")
        self.public_key = self.keypair[0]
        self.private_key = self.keypair[1]


def CA_sign(message, sign_hash=sha64):
    h = sign_hash(message)
    km = key_model()
    signature = rsa.core.encrypt_int(h, km.private_key.d, km.private_key.n)
    signature = signature.to_bytes(km.private_key.n.bit_length(), "big")
    signature = base64.b64encode(signature)
    signature = signature.decode("ASCII")
    return signature

def validate_CA_sign(message, signature, sign_hash=sha64):
    h = sign_hash(message)
    km = key_model()
    signature = signature.encode("ASCII")
    signature = base64.b64decode(signature)
    signature = int.from_bytes(signature, "big")
    h2 = rsa.core.decrypt_int(signature, km.public_key.e, km.public_key.n)
    return h == h2
=======
    return h==h2

# Utility functions
inverse_mod = rsa.common.inverse
>>>>>>> Kopi_branch
