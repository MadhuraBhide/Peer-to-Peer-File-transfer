import socket
import sys

def register(info, myport,IP):
    # Create a TCP/IP socket for Register request
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the RS server is listening
    self_IP = socket.gethostbyname(socket.gethostname())
    server_address = (IP, 65423)
    # status of the connection
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    try:
        # Send Register message
        message ='Register<sp>P2P-DI/1.0<sp>Host:{0}<sp>OS: Mac OS 10.4.1<el>'.format(info)
        sock.sendall(message)

        # Look for the response
        data = sock.recv(16)
        
        #ACK from RS server
        if data=="ok":
            d=['Host:{0}<sp>RFCPort:{1}<el>'.format(info,myport)]
            s=""
            s=s.join(d)
            sock.sendall(s)
            c= sock.recv(16)
    finally:
        print >>sys.stderr, 'closing Register socket close'
        sock.close()
    print('Got Cookie:{0}'.format(c))
    return(c)
