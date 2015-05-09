# -*- coding: utf-8 -*-


# [dependencies] #######################################################################################################

import byte_utils
import globals as g


# [Response] ###########################################################################################################

class Response:

    # [constructor] ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def __init__(self, request, tables):

        self.request = request
        self.tables  = tables
        self.bytes   = []

        self.create_mbap_header()

        if request.function_code == g.FUNC_01_READ_COIL_STATUS:
            self.create_pdu_fc01()
        elif request.function_code == g.FUNC_02_READ_INPUT_STATUS:
            self.create_pdu_fc02()
        elif request.function_code == g.FUNC_03_READ_HOLDING_REGISTERS:
            self.create_pdu_fc03()
        elif request.function_code == g.FUNC_04_READ_INPUT_REGISTERS:
            self.create_pdu_fc04()

    # [create_mbap_header] ---------------------------------------------------------------------------------------------

    def create_mbap_header(self):

        # transaction id
        ti_hi, ti_lo = byte_utils.from_u16(self.request.transaction_id)
        self.bytes.append(ti_hi)
        self.bytes.append(ti_lo)

        # protocol identifier
        pi_hi, pi_lo = byte_utils.from_u16(self.request.protocol_identifier)
        self.bytes.append(pi_hi)
        self.bytes.append(pi_lo)

        # message length
        ml_hi, ml_lo = byte_utils.from_u16(0)
        self.bytes.append(ml_hi)
        self.bytes.append(ml_lo)

        # unit id
        self.bytes.append(byte_utils.from_u8(self.request.unit_id))

    # [create_pdu_fc01] ------------------------------------------------------------------------------------------------

    def create_pdu_fc01(self):

        """
        Sample "Read Coil Status (fc01)" Request:
        00:14 00:00 00:06 01 01 15:20 00:25

        MBAP (MODBUS Application Header) Header:
            00:14 : Transaction ID - Master increases with on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            01    : Function Code
            15 20 : Start Reference
            00 25 : Register Count

        ----------------

        Sample "Read Coil Status (fc01)" Response:
        00:14 00:00 00:08 01 01 05 FF FF FF FF 1F

        MBAP (MODBUS Application Header) Header:
            00:14 : Transaction ID - Master increases with on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:08 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            01    : Function Code
            05    : Data Size
            FF    : 1 1 1 1 1 1 1 1 @ 1520
            FF    : 1 1 1 1 1 1 1 1 @ 1528
            FF    : 1 1 1 1 1 1 1 1 @ 1530
            FF    : 1 1 1 1 1 1 1 1 @ 1538
            1F    : 0 0 0 1 1 1 1 1 @ 1540
        """

        table_id   = 0
        byte_count = (self.request.register_count / 8 + 1)

        # function code
        self.bytes.append(byte_utils.from_u8(self.request.function_code))

        # data size
        self.bytes.append(byte_utils.from_u8(byte_count))

        # read data from config
        counter = 0
        bits    = ''

        for i in range(self.request.start_reference, self.request.register_count):

            if counter == 8:
                self.bytes.append(byte_utils.from_u8(int(bits, 2)))

                counter = 0
                bits    = ''

            bits = str(self.tables[table_id][i]) + bits
            counter += 1

        print bits
        self.bytes.append(byte_utils.from_u8(int(bits, 2)))

        # update message length
        self.bytes[4], self.bytes[5] = byte_utils.from_u16(len(self.bytes) - 6)

    # [create_pdu_fc02] ------------------------------------------------------------------------------------------------

    def create_pdu_fc02(self):

        """
        Sample "Read Input Status (fc02)" Request:
        00:01 00:00 00:06 01 02 23:40 00:19

        MBAP (MODBUS Application Header) Header:
            00:35 : Transaction ID - Master increases with on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            02    : Function Code
            23 40 : Start Reference
            00 19 : Register Count

        ----------------

        Sample "Read Input Status (fc02)" Response:
        00:14 00:00 00:07 01 02 04 FF FF FF 01

        MBAP (MODBUS Application Header) Header:
            00:14 : Transaction ID - Master increases with on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:07 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            02    : Function Code
            04    : Data Size
            FF    : 1 1 1 1 1 1 1 1 @ 2340
            FF    : 1 1 1 1 1 1 1 1 @ 2348
            FF    : 1 1 1 1 1 1 1 1 @ 2350
            01    : 0 0 0 0 0 0 0 1 @ 2358
        """

        table_id   = 1
        byte_count = (self.request.register_count / 8 + 1)

        # function code
        self.bytes.append(byte_utils.from_u8(self.request.function_code))

        # data size
        self.bytes.append(byte_utils.from_u8(byte_count))

        # read data from config
        counter = 0
        bits    = ''

        for i in range(self.request.start_reference, self.request.register_count):

            if counter == 8:
                self.bytes.append(byte_utils.from_u8(int(bits, 2)))

                counter = 0
                bits    = ''

            bits = str(self.tables[table_id][i]) + bits
            counter += 1

        print bits
        self.bytes.append(byte_utils.from_u8(int(bits, 2)))

        # update message length
        self.bytes[4], self.bytes[5] = byte_utils.from_u16(len(self.bytes) - 6)

    # [create_pdu_fc02] ------------------------------------------------------------------------------------------------

    def create_pdu_fc03(self):

        """
        Sample "Read Holding Registers (fc03)" Request:
        00:68 00:00 00:06 01 03 36:A0 00:0A

        MBAP (MODBUS Application Header) Header:
            00:68 : Transaction ID - Master increases with on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            03    : Function Code
            36 A0 : Start Reference
            00 0A : Register Count

        ----------------

        Sample "Read Holding Registers (fc03)" Response:
        00:68 00:00 00:17 01 03 14 00:0A 00:12 00:34 00:25 00:67 00:84 00:1A 00:C3 00:76 00:11

        MBAP (MODBUS Application Header) Header:
            00:68 : Transaction ID - Master increases with on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:17 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            03    : Function Code
            14    : Data Size
            00 0A : Data 01 @ 36A0
            00 12 : Data 02 @ 36A1
            00 34 : Data 03 @ 36A2
            00 25 : Data 04 @ 36A3
            00 67 : Data 05 @ 36A4
            00 84 : Data 06 @ 36A5
            00 1A : Data 07 @ 36A6
            00 C3 : Data 08 @ 36A7
            00 76 : Data 09 @ 36A8
            00 11 : Data 10 @ 36A9
        """

        table_id = 2

        # function code
        self.bytes.append(byte_utils.from_u8(self.request.function_code))

        # data size
        self.bytes.append(byte_utils.from_u8(self.request.register_count * 2))

        # read data from config
        for i in range(self.request.start_reference, self.request.register_count):
            dv_hi, dv_lo = byte_utils.from_u16(self.tables[table_id][i])
            self.bytes.append(dv_hi)
            self.bytes.append(dv_lo)

        # update message length
        self.bytes[4], self.bytes[5] = byte_utils.from_u16(len(self.bytes) - 6)

    # [create_pdu_fc02] ------------------------------------------------------------------------------------------------

    def create_pdu_fc04(self):

        """
        Sample "Read Input Registers (fc04)" Request:
        00:81 00:00 00:06 01 04 21:12 00:08

        MBAP (MODBUS Application Header) Header:
            00:81 : Transaction ID - Master increases with on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            04    : Function Code
            21 12 : Start Reference
            00 08 : Register Count

        ----------------

        Sample "Read Input Registers (fc04)" Response:
        00:81 00:00 00:13 01 04 10 00:0A 00:12 00:34 00:25 00:67 00:84 00:1A 00:C3

        MBAP (MODBUS Application Header) Header:
            00:81 : Transaction ID - Master increases with on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:13 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            04    : Function Code
            10    : Data Size
            00 0A : Data 01 @ 2112
            00 12 : Data 02 @ 2113
            00 34 : Data 03 @ 2114
            00 25 : Data 04 @ 2115
            00 67 : Data 05 @ 2116
            00 84 : Data 06 @ 2117
            00 1A : Data 07 @ 2118
            00 C3 : Data 08 @ 2119
        """

        table_id = 3

        # function code
        self.bytes.append(byte_utils.from_u8(self.request.function_code))

        # data size
        self.bytes.append(byte_utils.from_u8(self.request.register_count * 2))

        # read data from config
        for i in range(self.request.start_reference, self.request.register_count):
            dv_hi, dv_lo = byte_utils.from_u16(self.tables[table_id][i])
            self.bytes.append(dv_hi)
            self.bytes.append(dv_lo)

        # update message length
        self.bytes[4], self.bytes[5] = byte_utils.from_u16(len(self.bytes) - 6)

    # [out] ------------------------------------------------------------------------------------------------------------

    def out(self):
        return ''.join(x for x in self.bytes)
