import socket
import sys
import ast

def PQuery(cookie,IP):
    # Create a TCP/IP socket for PQuery
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the RS server is listening
    server_address = (IP, 65423)
    # status of the connection
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    try:
        # Send PQquery
        message ='PQuery<sp>P2P-DI/1.0<sp>OS: Mac OS 10.4.1<el>Cookie:{0}<el>'.format(cookie)
        sock.sendall(message)
        # Look for the response
        data = sock.recv(4096)
    finally:
        print >>sys.stderr, 'closing PQ socket close'
        sock.close()
    print(data)
    return(data)
