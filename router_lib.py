import socket
import select

__message = """@KopiCTF participants:
If you are reading this, please note that NOTHING in this module is meant to be
changed. Doing so may break the challenge (not in a good way).
This module "simulates" a router, but it's actually the one making connections.
That's all.
"""

HOST = "localhost"
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
            ready, _, _ = select.select(self.sock.values(), [], [])
            for s in ready:
                raw_msg = s.recv()
                if raw_msg is not None:
                    sock = s
                    break
        msg = Message(sock.source, sock.dest, raw_msg)
        return msg
    
    def send(self,  msg):
        sock = self.sock[msg.dest]
        sock.send(msg.msg)

class Message(object):
    """ Represents a message (packet) sent to the router.
        Fields: source, dest, msg
    """
    def __init__(self, source, dest, msg):
        self.source = source
        self.dest = dest
        self.msg = msg

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