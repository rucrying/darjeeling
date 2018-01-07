from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
from udpwkpf_io_interface import *
import time



if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port> <ultrasound#> <echo#> <trig#>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

IOT_Ultrasound_Echo = int(sys.argv[4])
IOT_Ultrasound_Trig = int(sys.argv[5])
initial_value = -1
init = 1
blocked = 0

class IOT_Ultrasound(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('IOT_Ultrasound')
        self.echo = pin_mode(IOT_Ultrasound_Echo, PIN_TYPE_DIGITAL, PIN_MODE_INPUT)
        self.trig = pin_mode(IOT_Ultrasound_Trig,PIN_TYPE_DIGITAL,PIN_MODE_OUTPUT)

    def send_pulse():
        digital_write(self.trig,1)
        time.sleep(0.001)
        digital_write(self.trig,0)

    def wait_echo(boolean):
        while digital_read(self.echo) != boolean:
            continue

    def get_dis():
        send_pulse()
        wait_echo(1)
        start = time.time()
        wait_echo(0)
        finish = time.time()
        return 170*(finish - start)*100  

    def update(self,obj,pID=None,val=None):
        try:
            current_value = get_dis()
            print "IOT_Ultrasound_Distance: %d" % current_value
            if init < 10:
                initial_value = current_value
                init = init + 1
            else:
                if abs(initial_value - current_value) > initial_value/3:
                    blocked = 1
                    obj.setProperty(0,1)
                else:
                    if blocked == 0:
                        obj.setProperty(0,0)
                    else:
                        blocked = 0
                        obj.setProperty(0,0)
        except IOError:
            print "Error"

if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            m = IOT_Ultrasound()
            self.addClass(m,0)
            self.obj_iot_ultrasound = self.addObject(m.ID)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
    device_cleanup()
