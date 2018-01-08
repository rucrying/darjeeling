from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
from udpwkpf_io_interface import *


part_num = 4

start=0
destination=2
blind_pos=1
have_blind=1
people_num= [0,0,0,0,0]
now_route=[]

if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port> <redlight#> <pin#>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

def calculate_route(destination):
	global now_route
	global blind_pos
        global people_num    
	if blind_pos==0:
                map_all=[1,2,3,4]
		clock_cost=0
		clock_route=[]
		counter_clock_cost=0
		counter_clock_route=[]
		for i in range(0,len(map_all)) :
                    counter_clock_cost+=1
		    counter_clock_cost+= people_num[map_all[i]]
		    counter_clock_route.append(map_all[i])
		    if (map_all[i]==destination):
	    	        break
		for i in range(len(map_all)-1,-1,-1):
		    clock_cost+=1
		    clock_cost+= people_num[map_all[i]]
	            clock_route.append(map_all[i])
	            if map_all[i]==destination:
			break
                print "clock:",clock_cost,"counter_clock",counter_clock_cost
		print "clock",clock_route
                print "counterclock",counter_clock_route
                if (clock_cost > counter_clock_cost):
                    
		    now_route = counter_clock_route
		else:
			now_route = clock_route
	else:
		map_all=[]		
		clock_cost=0
		clock_route=[]
		counter_clock_cost=0
		counter_clock_route=[]

		for i in range(0,4):
		    p=blind_pos+i
		    if p >4:
	    	        p=p-4
		    map_all.append(p)
                
		for i in range(0,len(map_all)) :
		    counter_clock_cost+=1
                    counter_clock_cost+= people_num[map_all[i]]
		    counter_clock_route.append(map_all[i])
		    if map_all[i]==destination:
			break
		clock_route.append(blind_pos)
                clock_cost+=(people_num[blind_pos]+1)
                for i in range(len(map_all)-1,-1,-1):
		    clock_cost+=1
                    clock_cost+= people_num[map_all[i]]
		    clock_route.append(map_all[i])
		    if map_all[i]==destination:
		    	break

		if (clock_cost > counter_clock_cost):
			now_route = counter_clock_route
		else:
			now_route = clock_route
                print "clock:",clock_cost,"counter_clock",counter_clock_cost
		print "clock",clock_route
                print "counterclock",counter_clock_route

class IOT_center(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('center')

    def update(self,obj,pID=None,val=None):
		global people_num
		global blind_pos 
		global start
		global destination
                global have_blind
		if (pID ==0):
                        if val >65530:
                            val=val-65536
			if(val!=0):
                            if(val>0):
		                people_num[abs(val)]+=1
                                if (abs(val)!=1):
                                    people_num[abs(val)-1]-=1
                            else:
		                people_num[abs(val)]-=1
                                if(abs(val)!=1):
                                    people_num[abs(val)-1]+=1
			    obj.setProperty(0,0)
                            
                                
                            if(have_blind):
			        calculate_route(destination)
			#print "val",val
		elif(pID ==1):
                    print "val=",val
                    if(val!=65535):
			blind_pos=val
 			if blind_pos==start:
				have_blind+=1
				calculate_route(destination)
				obj.setProperty(2,10*blind_pos+now_route[0])
			elif blind_pos==destination:
				have_blind==0
				obj.setProperty(2,100)
			else:
				calculate_route(destination)
				obj.setProperty(2,10*blind_pos+now_route[1])
                print "route:",now_route
		print "blind at:",blind_pos
		print "all place have :",people_num,"people"


if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            m = IOT_center()
            self.addClass(m,0)
            self.obj_iot_redlight = self.addObject(m.ID)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
    device_cleanup()
