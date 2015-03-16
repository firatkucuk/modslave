#!/usr/bin/env python2
# -*- coding: utf-8 -*-


# [dependencies] #######################################################################################################

import socket
import json

from modbus import request, response


# [globals] ############################################################################################################

tables  = [
    [0] * 65536,   # discreteOutputCoils - 0000 to FFFF - 65536 bits
    [0] * 65536,   # discreteInputContacts - 0000 to FFFF - 65536 bits
    [0] * 65536,   # analogOutputRegisters - 0000 to FFFF - 65535 words
    [0] * 65536    # analogInputRegisters - 0000 to FFFF - 65535 words
]


# [inject_analog_table] ##############################################################################################

def inject_analog_table(table_id, config_table):

    for index in config_table:
        reference = int(index)

        if config_table[index] > 65535 or config_table[index] < 0:
            tables[table_id][reference] = 0
        else:
            tables[table_id][reference] = int(config_table[index])


# [inject_discrete_table] ##############################################################################################

def inject_discrete_table(table_id, config_table):

    for index in config_table:
        reference = int(index)

        if config_table[index] > 0:
            tables[table_id][reference] = 1
        else:
            tables[table_id][reference] = 0


# [inject_config] ######################################################################################################

def inject_config():

    inject_discrete_table(0, config["tables"]["discreteOutputCoils"])
    inject_discrete_table(1, config["tables"]["discreteInputContacts"])
    inject_analog_table(2, config["tables"]["analogOutputRegisters"])
    inject_analog_table(3, config["tables"]["analogInputRegisters"])


# [main block] #########################################################################################################

if __name__ == "__main__":

    config  = json.load(open('modemu.json'))
    host    = config["listenAddress"]
    port    = config["listenPort"]
    backlog = 5
    size    = 1024

    inject_config()

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    socket_server.listen(backlog)

    while True:
        client, address = socket_server.accept()
        data            = client.recv(size)

        # print "connected"

        if data:
            req = request.Request(data)
            res = response.Response(req, tables)
            out = res.out()

            print "request : ", ':'.join(x.encode('hex') for x in data)
            print "response: ", ':'.join(x.encode('hex') for x in out)

            client.send(out)

        client.close()


