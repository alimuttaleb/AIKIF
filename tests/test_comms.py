#!/usr/bin/python3
# coding: utf-8
# test_bias.py

import unittest
import sys
import os
root_fldr = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + "aikif" )
sys.path.append(root_fldr)

import comms as mod_comms


dummy_comms = [
    {'key':'value'},
]


class CommsTest(unittest.TestCase):
    def tearDown(self):
        unittest.TestCase.tearDown(self)



    def test_01_channel(self):
        #self.comms = mod_bias.Bias(test_metadata)
        ch = mod_comms.Channel('audio', 'F57gj3thddj')
        #cm.add_channel(Channel('TCP', 'Jgfdedfsweewr54'), 'Jgfdedfsweewr54')
        #print(ch)

        self.assertTrue('audio : 0 incoming messages' in str(ch))

    def test_02_comms_manager(self):
        #self.comms = mod_bias.Bias(test_metadata)
        cm = mod_comms.CommsManager()
        self.assertTrue('---- CommsManager ----' in str(cm))
        cm.add_channel(mod_comms.Channel('text', '12345'), '12345')
        self.assertTrue('channel : text : 0 incoming messages' in str(cm))


if __name__ == '__main__':
    unittest.main()