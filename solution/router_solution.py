import rsa

import cert
import dhke
import router_lib

# To exit router after running it, press ctrl c and wait up to 10s.

CA_CERT = cert.Certificate.load("CA.crt")
FAKE_A_CERT = cert.Certificate.load("alice2.crt")
FAKE_B_CERT = cert.Certificate.load("bob2.crt")
with open("man.pem","rb") as f:
    MAN_PRI = rsa.PrivateKey.load_pkcs1(f.read())

class Attack():
    """Attack state machine. Welcome to libdw~
       Inherit this to make an Attacker. We've done this for you.
       (Or make your own way to attack, feel free to. Our suggestion may not
        be the optimal way.)
       
       states are called step here.
       
       In a step X, the functon stepX() will be run.
       stepX() functions should take in 1 argument, msg
       stepX() functions should output 2 values, (modified_msg, next_step)
    """
    def __init__(self):
        self.step = 1
    
    def handle_msg(self, msg):
        func_step = "step{}".format(self.step)
        func = getattr(self, func_step) # Function dispatch.
        new_msg, newstep = func(msg)
        self.step = newstep
        return new_msg

class AliceAttack(Attack):
    def step1(self, msg):
        p, g, ga = msg.msg["p"], msg.msg["g"], msg.msg["ga"]
        self.fake_bob_dhkey = dhke.DHKey(p, g)
        self.fake_bob_dhkey.compute_shared(ga)
        
        data = {"gb":self.fake_bob_dhkey.ga}
        data = cert.create_signed_dict(data, MAN_PRI, FAKE_B_CERT)
        msg = router_lib.Message("B", "A", data)
        
        return msg, 2
    
    def step2(self, msg):
        # Decrypt and drop message
        
        request = msg.msg["request"]
        iv = msg.msg["iv"]
        plaintext = dhke.aes256_dhke_decrypt(self.fake_bob_dhkey, request, iv)
        print("Request by Alice:")
        print(plaintext)
        
        return None, 3
    
    def step3(self, msg):
        return None, 3

class BobAttack(Attack):
    def step0(self):
        # Initialise the first message to Bob.
        self.fake_alice_dhkey = dhke.DHKey()
        
        p = self.fake_alice_dhkey.p
        g = self.fake_alice_dhkey.g
        ga = self.fake_alice_dhkey.ga
        
        data = {"p":p, "g":g, "ga":ga}
        data = cert.create_signed_dict(data, MAN_PRI, FAKE_A_CERT)
        msg = router_lib.Message("A", "B", data)
        
        return msg
    
    def step1(self, msg):
        gb = msg.msg["gb"]
        self.fake_alice_dhkey.compute_shared(gb)
        
        request = "Can I please have image#7258"
        ciphertext, iv = dhke.aes256_dhke_encrypt(self.fake_alice_dhkey, request)
        
        data = {"request":ciphertext, "iv":iv}
        msg = router_lib.Message("A", "B", data)
        
        return msg, 2
    
    def step2(self, msg):
        # Decrypt and drop message
        
        reply = msg.msg["reply"]
        iv = msg.msg["iv"]
        plaintext = dhke.aes256_dhke_decrypt(self.fake_alice_dhkey, reply, iv)
        print("FLAG:")
        print(plaintext)
        
        return None, 3
    
    def step3(self, msg):
        return None, 3



if __name__ == "__main__":
    router = router_lib.Router() # Initialise router. Don't change.
    
    # For you, THE MAN!
    alice_attack = AliceAttack()
    bob_attack = BobAttack()
    
    msg = bob_attack.step0()
    router.send(msg)
    # alice_attack.step=3 # Drop all alice messsages
    
    while True:
        msg = router.listen()
        
        print("-"*80)
        print(msg)
        
        if msg.source == "A":
            msg = alice_attack.handle_msg(msg)
        elif msg.source == "B":
            msg = bob_attack.handle_msg(msg)
        
        if msg is not None:
            router.send(msg)