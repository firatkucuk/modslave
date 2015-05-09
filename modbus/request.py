# -*- coding: utf-8 -*-


# [dependencies] #######################################################################################################

import byte_utils
import globals as g


# [Request] ############################################################################################################

class Request:

    """
        ----------------

        Sample "Read Coil Status (fc01 - fc0x01)" Request:
        00:14 00:00 00:06 01 01 15:20 00:25

        MBAP (MODBUS Application Header) Header:
            00:14 : Transaction ID - increased by Master on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            01    : Function Code
            15 20 : Start Reference
            00 25 : Register Count

        ----------------

        Sample "Read Input Status (fc02 - fc0x02)" Request:
        00:01 00:00 00:06 01 02 23:40 00:19

        MBAP (MODBUS Application Header) Header:
            00:35 : Transaction ID - increased by Master on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            02    : Function Code
            23 40 : Start Reference
            00 19 : Register Count

        ----------------

        Sample "Read Holding Registers (fc03 - fc0x03)" Request:
        00:01 00:00 00:06 01 03 36:A0 00:0A

        MBAP (MODBUS Application Header) Header:
            00:68 : Transaction ID - increased by Master on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            03    : Function Code
            36 A0 : Start Reference
            00 0A : Register Count

        ----------------

        Sample "Read Input Registers (fc04 - fc0x04)" Request:
        00:01 00:00 00:06 01 04 21:12 00:08

        MBAP (MODBUS Application Header) Header:
            00:81 : Transaction ID - increased by Master on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            04    : Function Code
            21 12 : Start Reference
            00 08 : Register Count

        ----------------

        Sample "Write Single Coil (fc05 - fc0x05)" Request:
        00:09 00:00 00:06 01 05 0B:B8 FF:00

        MBAP (MODBUS Application Header) Header:
            00:09 : Transaction ID - increased by Master on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            05    : Function Code
            0B B8 : Reference
            FF 00 : Data To Be Written (0xFF00: 1, 0x0000: 0)

        ----------------

        Sample "Write Single Register (fc06 - fc0x06)" Request:
        00:15 00:00 00:06 01 06 0F:A0 11:94

        MBAP (MODBUS Application Header) Header:
            00:15 : Transaction ID - increased by Master on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            06    : Function Code
            0F A0 : Start Reference
            11 94 : Data To Be Written

        ----------------

        Sample "Write Multiple Coils (fc15 - fc0x0F)" Request:
        00:19 00:00 00:08 01 0F 0F:A0 00:03 01 05

        MBAP (MODBUS Application Header) Header:
            00:19 : Transaction ID - increased by Master on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:08 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            0F    : Function Code
            0F A0 : Start Reference
            00 03 : Coil Count
            01    : Byte Count
            05    : Data To Be Written

        ----------------

        Sample "Write Multiple Registers (fc16 - fc0x10)" Request:
        00:21 00:00 00:0B 01 10 0F:A0 00:02 04 01:f4 03:E8

        MBAP (MODBUS Application Header) Header:
            00:21 : Transaction ID - increased by Master on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:0B : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            10    : Function Code
            0F A0 : Start Reference
            00 02 : Register Count
            04    : Byte Count
            01 F4 : Data 01
            03 E8 : Data 02
    """

    # [constructor] ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def __init__(self, data):

        data_bytes = list(data)

        self.transaction_id      = None  # 0 - 2
        self.protocol_identifier = None  # 2 - 4
        self.message_length      = None  # 4 - 6
        self.unit_id             = None  # 6
        self.function_code       = byte_utils.to_u8(data_bytes[7])  # 7
        self.start_reference     = None  # 8 - 10
        self.register_count      = None  # 10 - 12
        self.data_to_be_written  = []
        self.byte_count          = None

        self.read_mbap_header(data_bytes)

        if self.function_code == g.FUNC_01_READ_COIL_STATUS:
            self.read_pdu_for_all_read_functions(data_bytes)
        elif self.function_code == g.FUNC_02_READ_INPUT_STATUS:
            self.read_pdu_for_all_read_functions(data_bytes)
        elif self.function_code == g.FUNC_03_READ_HOLDING_REGISTERS:
            self.read_pdu_for_all_read_functions(data_bytes)
        elif self.function_code == g.FUNC_04_READ_INPUT_REGISTERS:
            self.read_pdu_for_all_read_functions(data_bytes)
        elif self.function_code == g.FUNC_05_WRITE_SINGLE_COIL:
            self.read_pdu_for_fc05(data_bytes)
        elif self.function_code == g.FUNC_06_WRITE_SINGLE_REGISTER:
            self.read_pdu_for_fc06(data_bytes)
        elif self.function_code == g.FUNC_15_WRITE_MULTIPLE_COILS:
            self.read_pdu_for_fc15(data_bytes)
        elif self.function_code == g.FUNC_16_WRITE_MULTIPLE_REGISTERS:
            self.read_pdu_for_fc16(data_bytes)
        else:
            raise Exception('Not implemented function')

    # [read_mbap_header] -----------------------------------------------------------------------------------------------

    def read_mbap_header(self, data_bytes):
        self.transaction_id      = byte_utils.to_u16(data_bytes[0:2])
        self.protocol_identifier = byte_utils.to_u16(data_bytes[2:4])
        self.message_length      = byte_utils.to_u16(data_bytes[4:6])
        self.unit_id             = byte_utils.to_u8(data_bytes[6])

    # [read_pdu_for_all_read_functions] --------------------------------------------------------------------------------

    def read_pdu_for_all_read_functions(self, data_bytes):
        self.start_reference = byte_utils.to_u16(data_bytes[8:10])
        self.register_count  = byte_utils.to_u16(data_bytes[10:12])

    # [read_pdu_for_fc05] ----------------------------------------------------------------------------------------------

    def read_pdu_for_fc05(self, data_bytes):
        self.start_reference = byte_utils.to_u16(data_bytes[8:10])
        incoming_data        = byte_utils.to_u16(data_bytes[10:12])
        mapped_value         = 0

        if incoming_data == 0xFF00:
            mapped_value = 1

        self.data_to_be_written = [mapped_value]

    # [read_pdu_for_fc06] ----------------------------------------------------------------------------------------------

    def read_pdu_for_fc06(self, data_bytes):
        self.start_reference    = byte_utils.to_u16(data_bytes[8:10])
        self.data_to_be_written = [byte_utils.to_u16(data_bytes[10:12])]

        print self.data_to_be_written

    # [read_pdu_for_fc15] ----------------------------------------------------------------------------------------------

    def read_pdu_for_fc15(self, data_bytes):
        self.start_reference    = byte_utils.to_u16(data_bytes[8:10])
        self.register_count     = byte_utils.to_u16(data_bytes[10:12])
        self.byte_count         = byte_utils.to_u16(data_bytes[12:13])

        # TODO: bit vector to data list

    # [read_pdu_for_fc16] ----------------------------------------------------------------------------------------------

    def read_pdu_for_fc16(self, data_bytes):
        self.start_reference    = byte_utils.to_u16(data_bytes[8:10])
        self.register_count     = byte_utils.to_u16(data_bytes[10:12])
        self.byte_count         = byte_utils.to_u8(data_bytes[12:13])
        self.data_to_be_written = []

        for i in range(self.byte_count / 2):
            value = byte_utils.to_u16(data_bytes[13 + (i * 2):15 + (i * 2)])
            self.data_to_be_written.append(value)