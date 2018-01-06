#!/usr/bin/python
import datetime
from unittest import TestLoader, TestSuite
from HTMLTestRunner import HTMLTestRunner
import os,sys,time
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'unit_tests/test_device'))

from test_location import TestLocation
from test_property import TestProperty
from test_discovery import TestDiscovery
from test_deploy import TestDeploy
from test_propagate import TestPropagate

if __name__ == '__main__':
	filename = datetime.datetime.now().strftime('report_%Hh_%Mm.html')
	date = datetime.datetime.now().strftime("%Y_%m_%d")

	try:
		os.mkdir('reports/%s' % (date))
	except:
		pass
	
	output = open('reports/%s/%s' % (date, filename), "wb")
	loader = TestLoader()
	suite = TestSuite((
			loader.loadTestsFromTestCase(TestLocation),
			loader.loadTestsFromTestCase(TestProperty),
			loader.loadTestsFromTestCase(TestDiscovery),
			loader.loadTestsFromTestCase(TestDeploy),
			loader.loadTestsFromTestCase(TestPropagate)
	))
	runner = HTMLTestRunner(stream=output, verbosity=1, title="WuKong Testing")
	runner.run(suite)
