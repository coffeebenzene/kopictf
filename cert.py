import json
import base64

import rsa
import hashlib

class Certificate():
    def __init__(self, subject_principal, rsa_pub, signature):
        if isinstance(rsa_pub, str) or isinstance(rsa_pub, bytes):
            rsa_pub = rsa.PublicKey.load_pkcs1(rsa_pub)
        if not isinstance(rsa_pub, rsa.PublicKey):
            raise Exception("Invalid rsa_pub")
        
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
    
    def as_dict(self):
        return {"subject_principal": self.subject_principal,
                "rsa_pub": self.rsa_pub.save_pkcs1().decode("ASCII"),
                "signature": self.signature,
               }
    
    def as_msg(self):
        return self.subject_principal + "|" + self.rsa_pub.save_pkcs1().decode("ASCII")
    
    def sign(self, CA_pri):
        """ Signs certificate. Will reset signature field. """
        msg = self.as_msg()
        self.signature = sign_rsa(msg, CA_pri)
        return self.signature
    
    def validate(self, CA_pub):
        msg = self.as_msg()
        return validate_rsa(msg, self.signature, CA_pub)
    
    @classmethod
    def load(cls, filename):
        with open(filename) as f:
            cert_json = json.load(f)
        return cls(**cert_json)
    
    def save(self, filename):
        with open(filename,"w") as f:
            json.dump(self.as_dict(), f)


# sign_hash is hash function for signing. Should convert str to int.
def sign_hash(msg):
    msg_bytes = msg.encode("UTF-8")
    h_bytes = hashlib.sha256(msg_bytes).digest()
    h = int.from_bytes(h_bytes, "big")
    return h

def bit_to_bytes(i):
    """i : number of bits
       return : number of bytes that fit i bits. (i.e. divide by 8, rounded up)
    """
    return (i+7)//8

def sign_rsa(message, rsa_pri):
    """message : str
       rsa_pri : rsa.PrivateKey
       return : signature (str)
    """
    h = sign_hash(message)
    h = h % rsa_pri.n # Fit into modulus keyspace
    signature = rsa.core.encrypt_int(h, rsa_pri.d, rsa_pri.n)
    size = bit_to_bytes(rsa_pri.n.bit_length())
    signature = signature.to_bytes(size, "big")
    signature = base64.b64encode(signature)
    signature = signature.decode("ASCII")
    return signature

def validate_rsa(message, signature, rsa_pub):
    """message : str
       signature : b64encoded str
       rsa_pub : rsa.PublicKey
       return: boolean (True if valid)
    """
    h = sign_hash(message)
    h = h % rsa_pub.n # Fit into modulus keyspace
    signature = signature.encode("ASCII")
    signature = base64.b64decode(signature)
    signature = int.from_bytes(signature, "big")
    h2 = rsa.core.decrypt_int(signature, rsa_pub.e, rsa_pub.n)
    return h==h2

def signed_json(data_dict, rsa_pri, cert):
    """data_dict : dict of fields to sign. 
                   Keys of dict must be strings.
                   "cert" and "signature" keys not allowed.
                   Values of dict must be either int or str.
       rsa_pri : Primary key to sign with
       cert : certificate containing public key corresponding to primary key.
       return : json_dict (str) containing signature and cert fields.
    """
    for k,v in data_dict.items():
        if not isinstance(k, str):
            raise ValueError("Invalid key, key is not string: {} : {}".format(k,v))
        if not isinstance(v, (int, str)):
            raise ValueError("Invalid value, must be int, str: {} : {}".format(k,v))
        if k in ("cert", "signature"):
            raise ValueError("Invalid key, 'cert' and 'signature' not allowed: {} : {}".format(k,v))
    
    msg_to_sign = json.dumps(data_dict, sort_keys=True)
    signature = sign_rsa(msg_to_sign, rsa_pri)
    json_dict = data_dict.copy()
    json_dict["signature"] = signature
    json_dict["cert"] = cert.as_dict()
    return json.dumps(json_dict, sort_keys=True)

def read_signed_json(json_dict):
    """json_dict : json dict as a str
       return : dict containing all fields of json_dict.
       DOES NOT VALIDATE.
    """
    return json.loads(json_dict)

# Utility functions
inverse_mod = rsa.common.inverse