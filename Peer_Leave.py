import socket
import sys

def leave(info,IP):
    # Create a TCP/IP socket for leave request
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the RS server is listening
    server_address = (IP, 65423)
    # status of the connection
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    try:
        # Send Leave message
        message ='Leave<sp>P2P-DI/1.0<sp>Mac OS 10.4.1<el>Cookie:{0}<el>'.format(info)
        sock.sendall(message)

        # Look for ACK the response
        data = sock.recv(16)
        
    finally:
        print >>sys.stderr, 'closing Leave socket close'
        sock.close()
