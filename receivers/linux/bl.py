# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
import time
import thread

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print "Waiting for connection on RFCOMM channel %d" % port


def read(client_sock):
    while True:
        try:
            data = client_sock.recv(1024)
            if len(data) == 0:
                raise IOError()
            dictk = {
                    'F5':'F5',
                    'Prev':'BackSpace',
                    'Next':'Return',
                    'Esc':'Escape'
                    }
            key = dictk.get(data, None)
            if key:
                os.popen('xte "key %s"'%key)
        except IOError:
            client_sock.close()

while True:
    client_sock, client_info = server_sock.accept()
    print "Accepted connection from ", client_info
    thread.start_new(read, (client_sock, ))



print "disconnected"

server_sock.close()
print "all done"
