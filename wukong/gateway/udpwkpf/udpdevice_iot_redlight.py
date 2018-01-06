from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
from udpwkpf_io_interface import *



init = 1 
initial_value = -1 
blocked = 0

if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port> <redlight#> <pin#>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)
IOT_Redlight_Pin = int(sys.argv[4])

class IOT_Redlight(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('IOT_Redlight')
        self.IO = pin_mode(IOT_Redlight_Pin, PIN_TYPE_DIGITAL, PIN_MODE_INPUT)

    def update(self,obj,pID=None,val=None):
        global initial_value
        global init
        global blocked
        try:
            current_value = digital_read(self.IO)
            print "IOT_Redlight value: %d" % current_value
            '''    
            if init < 10:
                initial_value = current_value
                obj.setProperty(0,-1)
                init = init + 1 
            else:
                if abs(initial_value - current_value) > initial_value/3:
                    blocked = 1
                    obj.setProperty(0,2+10*int(sys.argv[3])) 
                else:
                    if blocked == 0:
                        obj.setProperty(0,0+10*int(sys.argv[3]))
                    else:
                        blocked = 0
                        obj.setProperty(0,1+10*int(sys.argv[3]))
                        '''
            obj.setProperty(0,current_value) 
        except IOError:
            print "Error"

if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            m = IOT_Redlight()
            self.addClass(m,0)
            self.obj_iot_redlight = self.addObject(m.ID)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
    device_cleanup()
