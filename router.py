import router_lib
import cert

import json

CA_CERT = cert.Certificate.load("CA.crt")

router = router_lib.Router() # Initialise router. Don't change.

if __name__ == "__main__":
    while True:
        msg = router.listen()
        
        # Insert your code here. Example code given to simply print the msg.
        print("-"*79)
        print("source: {}".format(msg.source))
        print("dest: {}".format(msg.dest))
        # msg.msg is json encoded.
        msg_dict = json.loads(msg.msg)
        print("msg:")
        print(json.dumps(msg_dict, indent=4, sort_keys=True)) # pretty print
        
        router.send(msg)