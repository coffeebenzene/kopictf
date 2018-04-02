import router_lib
import cert

router = router_lib.Router() # Initialise router. Don't change.

if __name__ == "__main__":
    while True:
        msg = router.listen()
        
        # Insert your code here. Example code given to simply print the msg.
        print("-"*79)
        print("source: {}".format(msg.source))
        print("dest: {}".format(msg.dest))
        # msg.msg is json encoded.
        # Pretty printing it as an example:
        import json # bad practice! import at the top!
        msg_dict = cert.read_signed_json(msg.msg)
        print("msg:")
        print(json.dumps(msg_dict, indent=4, sort_keys=True))
        
        router.send(msg)