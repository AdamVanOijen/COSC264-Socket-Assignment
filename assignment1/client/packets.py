class DtRequest:
    DATE_REQUEST = 1
    TIME_REQUEST = 2
    HEADER_SIZE_BYTES = 6

    #indicies of the fields in the DtRequest packet bytearray
    field_index = {
        'MagicNo' : [0, 1],
        'PacketType' : [2, 3],
        'RequestType' : [4, 5]
    }

    def __init__(self, request):
        """Constructs a wrapper object for the DtRequest packet bytearray
        and fills the byte array with the necessary fields and their vaules"""
        if request == 'date':
            request_code = 1
        elif request == 'time':
            request_code = 2
        else:
            print("invalid request type")
            return None

        self.data = bytearray(self.HEADER_SIZE_BYTES)
        self.enter_field('MagicNo', 18814, 2) #18814 = 0x497E in decimal
        self.enter_field('PacketType', 1, 2)
        self.enter_field('RequestType', request_code, 2)
        
    def enter_field(self, field, value, n_bytes):
        """ fills the specified *field* of size *n_bytes* with *value* """

        value_bytes = (value).to_bytes(n_bytes, byteorder='big')
        field_list = self.field_index[field]
        for byte_index, index in enumerate(field_list):
            self.data[index] = value_bytes[byte_index]



class DtResponseIncoming:
    def __init__(self, data):
        """Constructs a wrapper for the DtResponse packet bytearray and
        verifies that the packet is a valid DtResponse packet"""
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
            'text' : [i for i in range(13, len(data))]
        }
        self.data = data
        self.is_valid = self._verify_data()

    def get_value(self, field):
        """returns the value stored in the packet at the given field"""

        result = 0
        field_list = self.field_index[field].copy()
        if field is 'text':
            text = self.data[13:]
            return text.decode("utf-8")
        field_list.reverse()
        for n_byte, index in enumerate(field_list):
            result += (self.data[index] << (8*n_byte))

        return result

    def _verify_data(self):
        """checks to see if incoming packet is a valid DtResponse packet...
        returns True if packet is valid and returns False if packet is
        invalid"""

        if len(self.data) < 13:
            print("response must be at least 13 bytes")
            return False

        if self.get_value('magicNo') != 18814:#18814 = 0x497E in decimal
            print("invalid magic number")
            return False

        if self.get_value('packetType') != 2:
            print("invalid packet type")
            return False

        if self.get_value('LanguageCode') not in range(1, 4):
            print("invalid language code")
            print(self.data)
            return False

        if self.get_value('year') >= 2100:
            print("invalid year")
            return False

        if self.get_value('month') not in range(1, 13):
            print("invalid month")
            return False

        if self.get_value('day') not in range(1, 32):
            print("invalid day")
            return False

        if self.get_value('hour') not in range(0, 24):
            print("invalid hour")
            return False

        if self.get_value('minute') not in range(0, 60):
            print("invalid minute")
            return False

        if (self.get_value('length') + 13) != len(self.data):
            print("invalid length field")
            return False

        return True

