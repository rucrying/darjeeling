from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
from udpwkpf_io_interface import *
import time
blind_pos=0
direction=[1,1]

class IOT_candle(WuClass):
    def __init__(self):
        R_pin = 3 
		G_pin = 5
		B_pin = 7
        WuClass.__init__(self)
        self.loadClass('candle')
        self.R_IO = pin_mode(R_Pin, PIN_TYPE_DIGITAL, PIN_MODE_INPUT)
        self.G_IO = pin_mode(G_Pin, PIN_TYPE_DIGITAL, PIN_MODE_INPUT)
        self.B_IO = pin_mode(B_Pin, PIN_TYPE_DIGITAL, PIN_MODE_INPUT)

    def update(self,obj,pID=None,val=None):
    	global blind_pos
    	global direction 
    	if (pID==0): #blind pos
    		if(val==100):
    			for i in range(0,5):
    				digital_write(self.R_IO,0)
    				digital_write(self.G_IO,0)
    				digital_write(self.B_IO,0)
    				time.sleep(0.1)
    				digital_write(self.R_IO,1)
    				digital_write(self.G_IO,1)
    				digital_write(self.B_IO,1)
    				time.sleep(0.1)


    		blind_pos=val/10
    		next_target=val%10
    		digital_write(self.R_IO,0)
    		digital_write(self.G_IO,0)
    		digital_write(self.B_IO,0)
    		time.sleep(3)
    		if(blind_pos==0):
    			direction=[1,1]
    			if(next_target==4):
    				direction=[0,1]
    				digital_write(self.R_IO,1)
    				digital_write(self.G_IO,0)
    				digital_write(self.B_IO,0)
    			elif (next_target ==1):
    				direction=[0,0]
    				digital_write(self.R_IO,0)
    				digital_write(self.G_IO,0)
    				digital_write(self.B_IO,1)
    		elif(blind_pos==1):
    			if(next_target==2):
    				if(direction==[0,0]):
    					digital_write(self.R_IO,1)
    					digital_write(self.G_IO,0)
    					digital_write(self.B_IO,0)
    				elif(direction==[1,0]):
						digital_write(self.R_IO,0)
    					digital_write(self.G_IO,1)
    					digital_write(self.B_IO,0)
    				direction=[1,1]		
    			elif(next_target==4):
    				if(direction==[0,0]):
    					digital_write(self.R_IO,0)
    					digital_write(self.G_IO,1)
    					digital_write(self.B_IO,0)
    				elif(direction==[1,0]):
						digital_write(self.R_IO,0)
    					digital_write(self.G_IO,0)
    					digital_write(self.B_IO,1)
    				direction=[0,1]
    		
    		elif(blind_pos==2):
    			if(next_target==3):
    				if(direction==[1,1]):
    					digital_write(self.R_IO,1)
    					digital_write(self.G_IO,0)
    					digital_write(self.B_IO,0)
    				elif(direction==[0,0]):
						digital_write(self.R_IO,0)
    					digital_write(self.G_IO,1)
    					digital_write(self.B_IO,0)
    				direction=[0,1]		
    			elif(next_target==1):
    				if(direction==[1,1]):
    					digital_write(self.R_IO,0)
    					digital_write(self.G_IO,1)
    					digital_write(self.B_IO,0)
    				elif(direction==[0,0]):
						digital_write(self.R_IO,0)
    					digital_write(self.G_IO,0)
    					digital_write(self.B_IO,1)
    				direction=[1,0]
    		
    		elif(blind_pos==3):
    			if(next_target==4):
    				if(direction==[1,1]):
    					digital_write(self.R_IO,0)
    					digital_write(self.G_IO,1)
    					digital_write(self.B_IO,0)
    				elif(direction==[0,1]):
						digital_write(self.R_IO,1)
    					digital_write(self.G_IO,0)
    					digital_write(self.B_IO,0)
    				direction=[1,0]		
    			elif(next_target==2):
    				if(direction==[1,1]):
    					digital_write(self.R_IO,0)
    					digital_write(self.G_IO,0)
    					digital_write(self.B_IO,1)
    				elif(direction==[0,1]):
						digital_write(self.R_IO,0)
    					digital_write(self.G_IO,1)
    					digital_write(self.B_IO,0)
    				direction=[0,0]
    		
    		elif(blind_pos==4):
    			if(next_target==3):
    				if(direction==[0,1]):
    					digital_write(self.R_IO,0)
    					digital_write(self.G_IO,0)
    					digital_write(self.B_IO,1)
    				elif(direction==[1,0]):
						digital_write(self.R_IO,0)
    					digital_write(self.G_IO,1)
    					digital_write(self.B_IO,0)
    				direction=[1,1]		
    			elif(next_target==1):
    				if(direction==[0,1]):
    					digital_write(self.R_IO,0)
    					digital_write(self.G_IO,1)
    					digital_write(self.B_IO,0)
    				elif(direction==[1,0]):
						digital_write(self.R_IO,1)
    					digital_write(self.G_IO,0)
    					digital_write(self.B_IO,0)
    				direction=[0,0]

if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            m = IOT_candle()
            self.addClass(m,0)
            self.obj_iot_redlight = self.addObject(m.ID)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
    device_cleanup()