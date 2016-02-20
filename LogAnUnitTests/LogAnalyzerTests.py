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

from LogAnalyzerModule import *
import unittest

# cut means by class under test mut means by method under test
class LogAnalyzerTestCase(unittest.TestCase):

	# firstly Directly test the @mut from @cut
	def test_IsValidLogFileName_BadExtension_ReturnFalse_0(self):
		logAnalyzer0 = LogAnalyzer_0()
		ret = logAnalyzer0.IsValidLogFileName('fn1.sl')
		self.assertFalse(ret)
	
	# However somethimes we have to rely on the extenal class or method
	# that we cannot control on it or it has not been finished yet
	# This is when we need stub to help us

	# Use constructor injection of stub
	# Assume we now rely on FakeExtendMgr_1 to verify if the file exists and valid
	# FakeExtendMgr1 is inheritaged from IExtensionMgr
	# This is what was done from book "artofunittest"
	def test_IsValidLogFileName_BadExtension_ReturnFalse_1(self):
		ext = FakeExtendMgr_1()
		ext.mWillBeValid = False
		logAnalyzer = LogAnalyzer_1(ext)
		ret = logAnalyzer.IsValidLogFileName('fn1.sl')
		self.assertFalse(ret)

	# Use constructor injection of stub
	# Assume we now rely on FakeExtendMgr_2 to verify if the file exists and valid
	# FakeExtendMgr2 is pure python class 
	# This is what I wrote because python is weak-type language
	# so it can still work without using inheratance
	def test_IsValidLogFileName_BadExtension_ReturnFalse_2(self):
		ext = FakeExtendMgr_2()
		ext.mWillBeValid = False

		logAnalyzer = LogAnalyzer_1(ext)
		ret = logAnalyzer.IsValidLogFileName('fn1.sl')

		self.assertFalse(ret)
	
	# Use Setter Injection of stub
	def test_IsValidLogFileName_BadExtension_ReturnFalse_3(self):
		ext = FakeExtendMgr_2()
		ext.mWillBeValid = False

		logAnalyzer = LogAnalyzer_2()
		logAnalyzer.SetIExtensionMgr(ext)
		ret = logAnalyzer.IsValidLogFileName('fn1.sl')

		self.assertFalse(ret)

	# Use Factory Injection of stub
	def test_IsValidLogFileName_BadExtension_ReturnFalse_4(self):
		ext = FakeExtendMgr_2()
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


class FakeExtendMgr_1(IExtensionMgr):
	def __init__(self):
		self.mWillBeValid = False
		return super().__init__()

	def IsValid(self,filename):
		return self.mWillBeValid

class FakeExtendMgr_2(object):
	def __init__(self):
		self.mWillBeValid = False

	def IsValid(self,filename):
		return self.mWillBeValid

if __name__ == '__main__': 
	unittest.main()