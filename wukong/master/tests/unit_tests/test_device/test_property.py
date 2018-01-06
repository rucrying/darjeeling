import os, sys
import time
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from test_environment_device import WuTest
from configuration import *
import random

class TestProperty(unittest.TestCase):

    def setUp(self):
        self.test = WuTest(False, False)

    def test_basic_propertyAPI(self):
        node_id = self.test.devs[0].node_id
        port = 3
        wuclassID = 2005
        property_number = 1
        datatype = 'short' # boolean, short, refresh_rate
        
        ans = random.randint(0, 255)
        self.test.setProperty(node_id, port, wuclassID, property_number, datatype, ans)
        time.sleep(SLEEP_SECS)
        res = self.test.getProperty(node_id, port, wuclassID, property_number)

        self.assertEqual(res, ans)

    
    def test_strength_propertyAPI(self):
        for i in xrange(TEST_PROPERTY_STRENGTH_NUMBER):
            node_id = self.test.devs[0].node_id
            port = 3
            wuclassID = 2005
            property_number = 1
            datatype = 'short'
            
            ans = random.randint(0, 255)      
            self.test.setProperty(node_id, port, wuclassID, property_number, datatype, ans)
            time.sleep(SLEEP_SECS)
            res = self.test.getProperty(node_id, port, wuclassID, property_number)

            self.assertEqual(res, ans)

if __name__ == '__main__':
    unittest.main()
