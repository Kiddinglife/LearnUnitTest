#!/usr/bin/env python 
#encoding: utf-8 

import sys
from LogAnalyzerModule import *
import unittest


# cut means by class under test mut means by method under test
class LogAnalyzerTestCase(unittest.TestCase):

	# No stub used just simply perform the test
	def test_IsValidLogFileName_BadExtension_ReturnFalse_NoStub(self):
		logAnalyzer0 = LogAnalyzer_0()
		ret = logAnalyzer0.IsValidLogFileName('fn1.sl')
		self.assertFalse(ret)
	
	# StubIjectedViaCtor 
	def test_IsValidLogFileName_BadExtension_ReturnFalse_StubIjectedViaCtor(self):
		ext = ExtendMgr_StubIjectedViaCtor()
		ext.mWillBeValid = False
		logAnalyzer = LogAnalyzer_StubInjectedViaCtor(ext)
		ret = logAnalyzer.IsValidLogFileName('fn1.sl')
		self.assertFalse(ret)

	# StubIjectedViaCtor
	# This is what I wrote because python is weak-type language
	# so it can still work without using inheratance
	def test_IsValidLogFileName_BadExtension_ReturnFalse_StubIjectedViaCtor_WithoutInhertingFrom_ExtensionMgr_AbstractedInterface(self):
		ext = StubIjectedViaCtor_WithoutIngeritingFrom_ExtensionMgr_AbstractedInterface()
		ext.mWillBeValid = False

		logAnalyzer = LogAnalyzer_StubInjectedViaCtor(ext)
		ret = logAnalyzer.IsValidLogFileName('fn1.sl')

		self.assertFalse(ret)
	
	# Use Setter Injection of stub
	def test_IsValidLogFileName_BadExtension_ReturnFalse_3(self):
		ext = StubIjectedViaCtor_WithoutIngeritingFrom_ExtensionMgr_AbstractedInterface()
		ext.mWillBeValid = False

		logAnalyzer = LogAnalyzer_2()
		logAnalyzer.SetIExtensionMgr(ext)
		ret = logAnalyzer.IsValidLogFileName('fn1.sl')

		self.assertFalse(ret)

	# Use Factory Injection of stub
	def test_IsValidLogFileName_BadExtension_ReturnFalse_4(self):
		ext = StubIjectedViaCtor_WithoutIngeritingFrom_ExtensionMgr_AbstractedInterface()
		ext.mWillBeValid = False
		ExtensionMgrFactory.SetExtMgr(ext)

		logAnalyzer = LogAnalyzer_3()
		ret = logAnalyzer.IsValidLogFileName('fn1.sl')

		self.assertFalse(ret)

	@unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
	def test_skipUnless(self):
		pass

	@unittest.skipIf(sys.platform.startswith("linux"), "requires Linux")
	def test_skipIf(self):
		pass


class ExtendMgr_StubIjectedViaCtor(ExtensionMgr_AbstractedInterface):
	def __init__(self):
		self.mWillBeValid = False
		return ExtensionMgr_AbstractedInterface.__init__(self)

	def IsValid(self,filename):
		return self.mWillBeValid

class StubIjectedViaCtor_WithoutIngeritingFrom_ExtensionMgr_AbstractedInterface(object):
	def __init__(self):
		self.mWillBeValid = False

	def IsValid(self,filename):
		return self.mWillBeValid

if __name__ == '__main__': 
	unittest.main()