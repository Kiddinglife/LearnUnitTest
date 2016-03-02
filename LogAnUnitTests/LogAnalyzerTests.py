#!/usr/bin/env python 
# encoding: utf-8 

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
        ext = ExtendMgrStub()
        ext.mWillBeValid = False
        logAnalyzer = LogAnalyzer_StubInjectedViaCtor(ext)
        ret = logAnalyzer.IsValidLogFileName('fn1.sl')
        self.assertFalse(ret)

    # StubIjectedViaCtor
    # This is what I wrote because python is weak-type language
    # so it can still work without using inheratance
    def test_IsValidLogFileName_BadExtension_ReturnFalse_StubIjectedViaCtor_WithoutInhertingFrom_ExtensionMgr_AbstractedInterface(self):
        ext = ExtendMgrStub_WithoutIngeritingFrom_ExtensionMgr_AbstractedInterface()
        ext.mWillBeValid = False

        logAnalyzer = LogAnalyzer_StubInjectedViaCtor(ext)
        ret = logAnalyzer.IsValidLogFileName('fn1.sl')

        self.assertFalse(ret)
    
    # StubInjectedViaPropertySetter
    def test_IsValidLogFileName_BadExtension_ReturnFalse_StubInjectedViaPropertySetter(self):
        ext = ExtendMgrStub()
        ext.mWillBeValid = False

        logAnalyzer = LogAnalyzer_StubInjectedViaPropertySetter()
        logAnalyzer.SetIExtensionMgr(ext)
        ret = logAnalyzer.IsValidLogFileName('fn1.sl')

        self.assertFalse(ret)

    # StubIjectedViaFactory
    def test_IsValidLogFileName_BadExtension_ReturnFalse_4_StubIjectedViaFactory(self):
        ext = ExtendMgrStub()
        ext.mWillBeValid = False
        ExtensionMgrFactory.SetExtMgr(ext)

        logAnalyzer = LogAnalyzer_StubInjectedViaFactory()
        ret = logAnalyzer.IsValidLogFileName('fn1.sl')

        self.assertFalse(ret)
        
    # StubIjectedViaLocalFactoryMethod
    def test_IsValidLogFileName_BadExtension_ReturnFalse_4_StubIjectedViaLocalFactoryMethod(self):
        ext = ExtendMgrStub()
        ext.mWillBeValid = False
        testableLogAnalyzer = TestableLogAnalyzer(ext)
        
if __name__ == '__main__': 
    unittest.main()
