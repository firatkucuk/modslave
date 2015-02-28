# -*- coding: utf-8 -*-


# [dependencies] #######################################################################################################

import byte_utils


# [globals] ############################################################################################################

FUNC_01_READ_COIL_STATUS          = 1
FUNC_02_READ_INPUT_STATUS         = 2
FUNC_03_READ_HOLDING_REGISTERS    = 3
FUNC_04_READ_INPUT_REGISTERS      = 4
FUNC_05_FORCE_SINGLE_COIL         = 5
FUNC_06_PRESET_SINGLE_REGISTER    = 6
FUNC_15_FORCE_MULTIPLE_COILS      = 15
FUNC_16_PRESET_MULTIPLE_REGISTERS = 16


# [Request] ############################################################################################################

class Request:

    """
        ----------------

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

        Sample "Read Holding Registers (fc03)" Request:
        00:01 00:00 00:06 01 03 36:A0 00:0A

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

        Sample "Read Input Registers (fc04)" Request:
        00:01 00:00 00:06 01 04 21:12 00:08

        MBAP (MODBUS Application Header) Header:
            00:81 : Transaction ID - Master increases with on every request
            00:00 : Protocol Identifier - 0 for MODBUS Standard Protocol
            00:06 : Message Length
            01    : Unit ID
        PDU (Protocol Data Unit):
            04    : Function Code
            21 12 : Start Reference
            00 08 : Register Count
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

        self.read_mbap_header(data_bytes)

        if self.function_code == FUNC_01_READ_COIL_STATUS:
            self.read_pdu_read_operation(data_bytes)
        elif self.function_code == FUNC_02_READ_INPUT_STATUS:
            self.read_pdu_read_operation(data_bytes)
        elif self.function_code == FUNC_03_READ_HOLDING_REGISTERS:
            self.read_pdu_read_operation(data_bytes)
        elif self.function_code == FUNC_04_READ_INPUT_REGISTERS:
            self.read_pdu_read_operation(data_bytes)
        else:
            raise Exception('Not implemented function')

    # [read_mbap_header] -----------------------------------------------------------------------------------------------

    def read_mbap_header(self, data_bytes):
        self.transaction_id      = byte_utils.to_u16(data_bytes[0:2])
        self.protocol_identifier = byte_utils.to_u16(data_bytes[2:4])
        self.message_length      = byte_utils.to_u16(data_bytes[4:6])
        self.unit_id             = byte_utils.to_u8(data_bytes[6])

    # [read_pdu_read_operation] ----------------------------------------------------------------------------------------

    def read_pdu_read_operation(self, data_bytes):
        self.start_reference = byte_utils.to_u16(data_bytes[8:10])
        self.register_count  = byte_utils.to_u16(data_bytes[10:12])