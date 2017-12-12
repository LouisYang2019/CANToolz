from cantoolz.module import CANModule


class firewall(CANModule):

    name = "Filter CAN messages"
    help = """

    This module block CAN messages by ID.

    Init parameters: None

    Module parameters:
        - 'white_list': [0x1, 0x2]  # List of CAN IDs that should be let through
        - 'black_list': [0x3, 0x4]  # List of CAN IDs that should be blocked
        - 'white_body': [[1, 2, 3, 4, 5, 6, 7, 8]]  # List of CAN message body that should be let through
        - 'black_body': [[8, 7, 6, 5, 4, 3, 2, 1]]  # List of CAN message body that should be blocked
        - 'hex_white_body': ['1122334455667788']  # List of CAN message body (in hex) that should be let through
        - 'hex_black_body': ['8877665544332211']  # List of CAN message body (in hex) that should be blocked
        - 'white_bus': ['pipe1', 'pipe2']  # List of pipes that should be let through
        - 'black_bus': ['pipe3', 'pipe4']  # List of pipes that should be blocked

    Example:
        {'white_list': [133,111]}

        {'black_body': [[42, 42, 42, 42], [11, 22, 33, 44, 55, 66, 77, 88]]}

        {'hex_white_body': ['1011121314', '0102030405060708]}

        {'black_bus': ['hw_USBTin']}

    """

    id = 4
    _active = True
    version = 1.0

    # Effect (could be fuzz operation, sniff, filter or whatever)
    def do_effect(self, can, args):
        if can.data is not None:
            if 'black_list' in args and can.id in args.get('black_list', []):
                can.data = None
                self.dprint(2, "Message " + str(can.id) + " has been blocked(BL) (BUS = " + str(can.bus) + ")")
            elif 'white_list' in args and can.id not in args.get('white_list', []):
                can.data = None
                self.dprint(2, "Message " + str(can.id) + " has been blocked(WL) (BUS = " + str(can.bus) + ")")
            if 'white_body' in args and can.data not in args.get('white_body', []):
                can.data = None
                self.dprint(2, "Message " + str(can.id) + " has been blocked(WB) (BUS = " + str(can.bus) + ")")
            elif 'black_body' in args and can.data in args.get('black_body', []):
                can.data = None
                self.dprint(2, "Message " + str(can.id) + " has been blocked(BB) (BUS = " + str(can.bus) + ")")
            if 'hex_white_body' in args and self.get_hex(can.raw_data) not in args.get('hex_white_body', []):
                can.data = None
                self.dprint(2, "Message " + str(can.id) + " has been blocked(WB) (BUS = " + str(can.bus) + ")")
            elif 'hex_black_body' in args and self.get_hex(can.raw_data) in args.get('hex_black_body', []):
                can.data = None
                self.dprint(2, "Message " + str(can.id) + " has been blocked(BB) (BUS = " + str(can.bus) + ")")
            if 'black_bus' in args and can.bus.strip() in args.get('black_body', []):
                can.data = None
                self.dprint(2, "Message " + str(can.id) + " has been blocked(BBus) (BUS = " + str(can.bus) + ")")
            elif 'white_bus' in args and can.bus.strip() not in args.get('white_bus', []):
                can.data = None
                self.dprint(2, "Message " + str(can.id) + " has been blocked(WBus) (BUS = " + str(can.bus) + ")")
        return can
