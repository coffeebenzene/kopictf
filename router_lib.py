import socket
import select
import json

__message = """@KopiCTF participants:
If you are reading this, please note that NOTHING in this module should be
changed. Doing so may break the challenge (not in a good way).
This module "simulates" a router, but it's actually the one making connections.
That's all.
You don't necessarily need to understand this module to complete the challenge.

btw. cert.py and dhke.py also shouldn't be changed. But it might be nice to 
understand what they do.
"""

#HOST = socket.gethostname() # For local testing.
HOST = "ec2-13-250-112-26.ap-southeast-1.compute.amazonaws.com"
ALICE_ADDR = (HOST, 64127)
BOB_ADDR = (HOST, 37590)

class Router(object):
    """Simulates router."""
    
    def __init__(self):
        self.sock = {}
        
        sock_alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_alice.connect(ALICE_ADDR)
        self.sock["A"] = SocketWrapper(sock_alice)
        self.sock["A"].set_source_dest("A", "B")
        
        sock_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_bob.connect(BOB_ADDR)
        self.sock["B"] = SocketWrapper(sock_bob)
        self.sock["B"].set_source_dest("B", "A")
    
    def listen(self):
        """Waits until a message is sent to the router.
           If multiple are available, select the one to receive arbitarily.
           returns : Message object (has .source, .dest, .msg fields)
        """
        # Also simulates message forwarding.
        # Source and destinations are created by router, not set by sender.
        raw_msg = None
        while raw_msg is None: # Take care of suprious receive.
            # Allow timeout in select to allow interrupts.
            ready, _, _ = select.select(self.sock.values(), [], [], 10)
            for s in ready:
                raw_msg = s.recv()
                if raw_msg is not None:
                    sock = s
                    break
        msg_data = json.loads(raw_msg.decode("utf-8"))
        msg = Message(sock.source, sock.dest, msg_data)
        return msg
    
    def send(self,  msg):
        sock = self.sock[msg.dest]
        raw_msg = json.dumps(msg.msg).encode("utf-8")
        sock.send(raw_msg)

class Message(object):
    """ Represents a message (packet) sent to the router.
        Fields: source, dest, msg (dict of data)
    """
    def __init__(self, source, dest, msg_data):
        self.source = source
        self.dest = dest
        self.msg = msg_data
    
    def __repr__(self):
        template = ('Message(\n'
                   '  source={},\n'
                   '  dest={},\n'
                   '  msg={}\n)')
        str_self = template.format(repr(self.source),
                                   repr(self.dest),
                                   repr(self.msg),
                                  )
        return str_self

class SocketWrapper(object):
    def __init__(self, s):
        s.settimeout(10)
        self.s = s
    
    def set_source_dest(self, source, dest):
        self.source = source
        self.dest = dest
    
    def fileno(self): # to enable select()
        return self.s.fileno()
    
    def send(self, msg):
        l = len(msg)
        if l >= 4294967296: # 256**4 max size. Must be strictly smaller.
            raise OverflowError("Message to big")
        l = l.to_bytes(4, "big")
        msg = l + msg
        self.s.sendall(msg)
    
    def recv(self):
        l = self.s.recv(4)
        if len(l) == 0: # Spurious receive. Return None
            return None
        elif len(l) != 4:
            raise Exception("Message length field truncated: {}".format(l))
        l = int.from_bytes(l,"big")
        to_read = l
        total_msg = []
        while to_read > 0:
            bytes_to_read = min(to_read, 4096)
            msg = self.s.recv(bytes_to_read)
            to_read -= len(msg)
            total_msg.append(msg)
        total_msg =  b"".join(total_msg)
        return total_msg