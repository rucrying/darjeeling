import serial
import time
import gevent

class AutoNet:
    def __init__(self, transport_learn_functions):
        self.port = serial.Serial(baudrate=38400, timeout=1.0, port="/dev/ttyUSB0")
        self._add_device = transport_learn_functions['a']
        self._delete_device = transport_learn_functions['d']
        self._stop_learning = transport_learn_functions['s']

    def _read_number(self):
        c = port.read()
        if c != '':
            return ord(c)
        return 0

    def get_gateway_mac_address(self):
        while True:
            command = ReadNumber()
            if command == 1:
                num = ReadNumber()
                device_list = []
                for i in xrange(num):
                    device_list.append(ReadNumber())
                # TODO: mac_address should be a list with 8 items of 1 byte!
                gateway_mac_address = device_list[0]
                break
            time.sleep(0.01)
        return gateway_mac_address

    def serve_autonet(self):
        while True:
            command = ReadNumber()
            if command == 1:
                num = ReadNumber()
                device_list = []
                for i in xrange(num):
                    device_list.append(ReadNumber())

            elif command == 2: # add
                new_device_mac_address = ReadNumber()
                self._add_device()

            elif command == 3: # delete
                del_device_mac_address = ReadNumber()
                self._delete_device()
            gevent.sleep(0.01)