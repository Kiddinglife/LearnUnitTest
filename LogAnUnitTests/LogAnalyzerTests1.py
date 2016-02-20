#!/usr/bin/env python 
#encoding: utf-8 

import sys
if not "../LogAnProject" in sys.path:
    sys.path.append("../LogAnProject")
if not 'LogAnalyzerModule' in sys.modules:
    LogAnalyzer = __import__('LogAnalyzerModule')
else:
    eval('import LogAnalyzerModule')
    LogAnalyzer = eval('reload(LogAnalyzerModule)')

from LogAnalyzerModule import LogAnalyzer
import unittest

#Such a working environment for the testing code is called a fixture.
#Test case instances are grouped together according to the features they test.
#unittest provides a mechanism for this: the test suite, represented by
#unittest??s TestSuite class.  In most cases, calling unittest.main()
#will do the right thing and collect all the module??s test cases for you, and
#then execute them.
class LogAnalyzerTestCase1(unittest.TestCase):
	def test_IsValidLogFileName_BadExtension_ReturnFalse(self):
		logAnalyzer = LogAnalyzer()
		ret = logAnalyzer.IsValidLogFileName('fn1.sln')
		self.assertFalse(not ret)

	@unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
	def test_skipUnless(self):
		pass

	@unittest.skipIf(sys.platform.startswith("linux"), "requires Linux")
	def test_skipIf(self):
		pass

if __name__ == '__main__': 
	unittest.main()