from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
from udpwkpf_io_interface import *


if len(sys.argv) <= 2:
    print 'python %s <gip> <dip>:<port> <redlight#> <pin#>' % sys.argv[0]
    print '      <gip>: IP addrees of gateway'
    print '      <dip>: IP address of Python device'
    print '      <port>: An unique port number'
    print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
    sys.exit(-1)

man_count_pin=int(sys.argv[3])

censor_status=[0,0]
direction=0
class man_count(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('man_count')

    def update(self,obj,pID=None,val=None):
        global direction
        if (val ==0):
            if censor_status[0]==1 and censor_status[1]==1:
                obj.setProperty(2,0)
                obj.setProperty(2,direction*man_count_pin)
                censor_status[0]=0
                censor_status[1]=0
                print "ID:",man_count_pin,direction
        if (val != 0):
            if (pID ==0):
                if(0<val<30):
                    status = val%10
                if censor_status[1]==0:
                    censor_status[0]=1;
                    direction=1
                elif censor_status[1] == 1:
                    censor_status[0]=1
            elif(pID == 1):
                status = val%10
                if censor_status[0]==0:
            	    censor_status[1]=1;
                    direction=-1
                elif censor_status[0] == 1:
                    censor_status[1]=1

if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            m = man_count()
            self.addClass(m,0)
            self.obj_iot_redlight = self.addObject(m.ID)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
    device_cleanup()
