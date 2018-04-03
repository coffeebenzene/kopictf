import router_lib
import cert
import dhke

CA_CERT = cert.Certificate.load("CA.crt")


if __name__ == "__main__":
    router = router_lib.Router() # Initialise router. Don't change.
    
    while True:
        msg = router.listen()
        
        # Insert your code here. Example code given to simply print the msg.
        print("-"*79)
        print("source: {}".format(msg.source))
        print("dest: {}".format(msg.dest))
        # msg.msg is a dict. Pretty print as example
        import pprint
        print("msg:")
        pprint.pprint(msg.msg)
        
        router.send(msg)