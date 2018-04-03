import rsa

import cert
import dhke
import router_lib

CA_CERT = cert.Certificate.load("CA.crt")
# Example to load pem file (rsa private key)
#with open("man.pem","rb") as f:
#    MAN_PRI = rsa.PrivateKey.load_pkcs1(f.read())

class Attack():
    """Attack state machine. Welcome to libdw~
       Inherit this to make an Attacker. We've done this for you.
       (Or make your own way to attack, feel free to)
       
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
        return msg, 1

class BobAttack(Attack):
    def step1(self, msg):
        return msg, 1



if __name__ == "__main__":
    router = router_lib.Router() # Initialise router. Don't change.
    
    # For you, THE MAN!
    alice_attack = AliceAttack()
    bob_attack = BobAttack()
    
    while True:
        msg = router.listen()
        
        # Insert your code here, or modify the AliceAttack and BobAttack classes.
        # Example code given to simply print the msg.
        print("-"*79)
        print("source: {}".format(msg.source))
        print("dest: {}".format(msg.dest))
        # msg.msg is a dict. Keys MUST be str, values MUST be int or str.
        # Pretty print as example
        import pprint
        print("msg:")
        pprint.pprint(msg.msg)
        # example modification
        # msg.msg["new_field"] = 123
        
        if msg.source == "A":
            msg = alice_attack.handle_msg(msg)
        elif msg.source == "B":
            msg = bob_attack.handle_msg(msg)
        
        if msg is not None:
            router.send(msg)