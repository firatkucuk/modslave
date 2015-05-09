#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("192.168.1.66", 1502))

data = [
    chr(0x00), chr(0x12),  # Transaction ID - Master increases with on every request
    chr(0x00), chr(0x00),  # Protocol Identifier - 0 for MODBUS Standard Protocol
    chr(0x00), chr(0x06),  # Message Length
    chr(0x01),             # Unit ID
    chr(0x03),             # Function Code
    chr(0x17), chr(0x70),  # Start Reference
    chr(0x00), chr(0x06)   # Register Count
]

s.send(''.join(data))
received_data = s.recv(1024)
s.close
print list(received_data)
