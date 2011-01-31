#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the Bluetooth Note Controller project
#
# Copyright (c) 2006-2009 Marco Antonio Islas Cruz
#
# Bluetooth Note Controller is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Bluetooth Note Controller is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# @category  Multimedia
# @package   Bluetooth Note Controller
# @author    Marco Antonio Islas Cruz <markuz@islascruz.org>
# @copyright 2010-211 Marco Antonio Islas Cruz
# @license   http://www.gnu.org/licenses/gpl.txt

# inspired on the work by Albert Huang <albert@csail.mit.edu>

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
