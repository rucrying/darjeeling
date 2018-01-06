from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
from udpwkpf_io_interface import *
import numpy as np

part_num = 4

start=0
destination=2
blind_pos=0
have_blind=0
people_num= np.zeros(part_num+1)
now_route=[]

if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port> <redlight#> <pin#>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

def calculate_route(start,destination):
	global now_route
	map_all=[1,2,3,4]
	if start==0:
		clock_cost=0
		clock_route=[]
		counter_clock_cost=0
		counter_clock_route=[]
		for i in range(0,size(map_all)) :
			counter_clock_cost+=1
			counter_clock_cost+= people_num[map_all[i]]
			counter_clock_route.append(i)
			if map_all[i]==destination:
				break
		for i in range(size(map_all)-1,-1,-1):
			clock_cost+=1
			clock_cost+= people_num[map_all[i]]
			clock_route.append(i)
			if map_all[i]==destination:
				break
		if (clock_cost > counter_clock_route):
			now_route = counter_clock_route
		else:
			now_route = clock_route
	else:
		map_all=[]		
		clock_cost=0
		clock_route=[]
		counter_clock_cost=0
		counter_clock_route=[]

		for i in range(0:4):
			p=start+i
			if p ==5:
				p=1
			map_all.append(i)

		counter_clock_route=[]
		for i in range(0,size(map_all)) :
			counter_clock_cost+= people_num[map_all[i]]
			counter_clock_route.append(i)
			if map_all[i]==destination:
				break
		for i in range(size(map_all)-1,-1,-1):
			clock_cost+= people_num[map_all[i]]
			clock_route.append(i)
			if map_all[i]==destination:
				break

		if (clock_cost > counter_clock_route):
			now_route = counter_clock_route
		else:
			now_route = clock_route


class IOT_center(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('center')

    def update(self,obj,pID=None,val=None):

		global people_num
		global blind_pos 
		global start
		global destination
		if (pID ==0):
			if(val!=0):
				people_num[abs(val)]+=val
				if abs(val)!=1:
					people_num[abs(val)-1]-=val
				if(have_blind):
					calculate_route(blind_pos,destination)
			print "route:",route
			print "blind at:",blind_pos
			print "all place have :",people_num,"people"
		elif(pID ==1):
			blind_pos=val
 			if blind_pos==start:
				have_blind+=1
				calculate_route(blind_pos,destination)
				obj.setProperty(3,now_route[0])
			elif blind_pos==destination:
				have_blind-=1
			else:
				calculate_route(blind_pos,destination)
				obj.setProperty(3,now_route[1])

        except IOError:
            print "Error"

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