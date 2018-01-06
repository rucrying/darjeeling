from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
from udpwkpf_io_interface import *



if len(sys.argv) <= 2:
	print 'python %s <gip> <dip>:<port> <magnetic#> <pin#>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)
IOT_Magnetic_Pin = int(sys.argv[4])

class IOT_Magnetic(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('IOT_Magnetic')
        self.IO = pin_mode(IOT_Magnetic_Pin, PIN_TYPE_DIGITAL, PIN_MODE_INPUT)

    def update(self,obj,pID=None,val=None):
        try:
            current_value = digital_read(self.IO)
            if current_value == 1:
                obj.setProperty(0,int(sys.argv[3]))
            elif current_value == 0:
                obj.setProperty(0,-1)                                           
            else:
                print "current_value error"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
            print "IOT_Magnetic value: %d" % current_value
        except IOError:
            print "Error"

if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            m = IOT_Magnetic()
            self.addClass(m,0)
            self.obj_iot_magnetic = self.addObject(m.ID)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
    device_cleanup()
