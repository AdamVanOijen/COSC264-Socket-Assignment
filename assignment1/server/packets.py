class DtRequestIncoming:
    """wrapper for the DtRequest bytearray"""
    def __init__(self, data):
        """constructs a wrapper object for the DtRequest bytearray and
        checks that the packet is a valid DtRequest packet"""
        self.data = data
        self.field_index = {
            'MagicNo': [0, 1],
            'PacketType': [2, 3],
            'RequestType': [4, 5]
        }
        self.is_valid = self._verify_packet()

    def get_value(self, field):
        """returns the value stored in the packet at the given field"""

        result = 0
        field_list = self.field_index[field].copy()
        field_list.reverse()
        for n_byte, index in enumerate(field_list):
            result += (self.data[index] << (8*n_byte))

        return result

    def _verify_packet(self):
        """checks to see if incoming packet is valid... returns True if
        packet is valid and returns False if packet is invalid"""

        if len(self.data) != 6:
            print("invalid packet size")
            return False

        #if ((self.data[0] << 8) + self.data[1]) != 18814:#18814 = 0x497E in decimal
        if self.get_value('MagicNo') != 18814:
            print("invalid magic number")
            return False

        #if ((self.data[2] << 8) + self.data[3]) != 1:
        if self.get_value('PacketType') != 1:
            print("invalid packet type")
            return False

        #request_type = (self.data[4] << 8) + self.data[5]
        #if (request_type != 1) and (request_type != 2):
        request_type = self.get_value('RequestType')
        if (request_type != 1) and (request_type != 2):
            print("invalid request type")
            return False

        return True


class DtResponseOutgoing:
    """wrapper for the DtResponse bytearray"""
    ENGLISH = 1
    MAORI = 2
    GERMAN = 3

    HEADER_SIZE_BYTES = 13

    def __init__(self, language_code, year, month, day, hour, minute, length, text):
        """Constructs a wrapper object for a DtResponse packet bytearray and
        fills the bytearray with the necessary fields and their values"""
        #indicies of the fields in the DtResponse packet bytearray
        self.field_index = {
            'magicNo': [0, 1],
            'packetType': [2, 3],
            'LanguageCode': [4, 5],
            'year': [6, 7],
            'month': [8],
            'day': [9],
            'hour' : [10],
            'minute' : [11],
            'length' : [12],
            'text' : [i for i in range(13, 13+length)]
        }

        self.data = bytearray(self.HEADER_SIZE_BYTES + length)
        self.enter_field('magicNo', 18814, 2) #18814 = 0x497E in decimal
        self.enter_field('packetType', 2, 2)
        self.enter_field('LanguageCode', language_code, 2)
        self.enter_field('year', year, 2)
        self.enter_field('month', month, 1)
        self.enter_field('day', day, 1)
        self.enter_field('hour', hour, 1)
        self.enter_field('minute', minute, 1)
        self.enter_field('length', length, 1)
        self.enter_field('text', text, length)

    def enter_field(self, field, value, n_bytes):
        """ fills the specified *field* of size *n_bytes* with *value* """

        if field == 'text':
            value_bytes = value.encode('utf-8')
        else:
            value_bytes = (value).to_bytes(n_bytes, byteorder='big')

        field_list = self.field_index[field]
        for byte_index, index in enumerate(field_list):
            self.data[index] = value_bytes[byte_index]
