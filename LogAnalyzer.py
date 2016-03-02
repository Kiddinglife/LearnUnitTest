#!/usr/bin/env python 
# encoding: utf-8 

import unittest

"""
the simplyest way to test return value 
No needs to use stub
"""
class LogAnalyzer_0(object):
    def IsValidLogFileName(self, fileName):
        return str(fileName).endswith('.sln')
"""
However somethimes we have to rely on the extenal class or method 
that we cannot control on it or it has not been finished yet
This is when we need stub to help us. eg, draw_from_weighted_range() and randrange(), interacting with filesystem. 
Fakes here include stub (assert on CUT) and mock (assert on Fake) we talk about stub and mock in later posts.
Say our IsValidLogFileName() method needs read through the config file and return true if extension is supported in config file,

There two big types to inject fakes into MUT(Method Under Test):
1.Test are performed on the MUT itself (eg. assert(mut.dosomething(),true)
    1.1 Abstracting concrete objects into interfaces or delegates
        How: Extract an interface to allow replacing or extending underlying impl
    1.2 Refactoring to allow injection of faked implementations of those delegates or interface.
        How: 
        1.2.1.Inject stub in code under test using factory design (layer of indirection 2 faking a member in factory class)
              the difference is that the object initiating the stub request is the code under test.
              the fake instances was set by code external to the code under test before the test started in the below.
              A test configures the factory class to re turn a stub object. The class usess the factory class to get the 
              stub instance, which in production code would return an object that is not a stub
              Preferred to using this layer
        1.2.2 Injection of a stub in test code (layer of indiretion 1 faking a member in class under test)
            1.2.2.1 Inject stub via ctor (cumbersome whenyou have many dependencies)
            1.2.2.2 Inject stub via setter/getter
                        This is much simpler than ctor injection as each test can set only the dependencies
                        that it needs to get the test underway;
                        Use this when you want to signify that the dependency is optional or the dependency has 
                        a default instance created that does not create any problems;
                
        1.2.4.Inject stub impl via parameter
2.Test are performed on the class that inhetites from MUT (eg. assert(mut_child.dosomething(),true)
    It is also known as Extract and override, which is is good to for sumulating inputs into your code under test
    (in other words, return values from dependency). but it is cumbersome when you want t verify and check interactions 
    that are coming out of the code under test int othe dependency (in other words, it is good to play stub but very bad to play mock)
    
    2.1 use local virtual factory method to get instance of stub
        The time not to use this is there is an interface ready to fake or there is already a place that seam can be injected.
    2.2 use extract and override to return a logical result instead of calling an actual denpendency
        This uses a simple faked result instead of a stub
        Much easier than 2.1 preferred to use
"""

# Refered to "1.1 Abstracting concrete objects into interfaces or delegates"
class ExtensionMgr_AbstractedInterface(object):
    def IsValid(self, filename):  # should be overwriten by child 
        pass

class FileExtensionMgr_ConcreteImpl(ExtensionMgr_AbstractedInterface):
    def IsValid(self, filename): 
        return str(filename).endswith('.sln') 

# Stubs    
class ExtendMgrStub(ExtensionMgr_AbstractedInterface):
    def __init__(self):
        self.mWillBeValid = False
        return ExtensionMgr_AbstractedInterface.__init__(self)

    def IsValid(self, filename):
        return self.mWillBeValid

class ExtendMgrStub_WithoutIngeritingFrom_ExtensionMgr_AbstractedInterface(object):
    def __init__(self):
        self.mWillBeValid = False

    def IsValid(self, filename):
        return self.mWillBeValid

    
# Refered to 1.2.2.1 Inject stub impl via ctor (cumbersome whenyou have many dependencies) 
class LogAnalyzer_StubInjectedViaCtor(object):
    def __init__(self, iExtensionMgr):
        self.mIExtensionMgr = iExtensionMgr

    def IsValidLogFileName(self, fileName):
        self.mIExtensionMgr.IsValid(fileName)
        
# Refered to "1.2.2.2 Inject stub impl via a setter and ggeter"
class LogAnalyzer_StubInjectedViaPropertySetter(object):
    def __init__(self):
        self.mIExtensionMgr = FileExtensionMgr_ConcreteImpl()

    def IsValidLogFileName(self, fileName):
        self.mIExtensionMgr.IsValid(fileName)

    def SetIExtensionMgr(self, ext):
        self.mIExtensionMgr = ext
        
    def GetIExtensionMgr(self):
        return self.mIExtensionMgr

# Refered to "1.2.1.Inject stub in code under test using factory design"
class ExtensionMgrFactory(object):
    iExtMgr = None

    @staticmethod
    def Create():
        # define factory that can use and return custom manager instance
        if ExtensionMgrFactory.iExtMgr is None:
            ExtensionMgrFactory.iExtMgr = FileExtensionMgr_ConcreteImpl()
        else:
            return ExtensionMgrFactory.iExtMgr

    @staticmethod
    def SetExtMgr(extmgr):
        ExtensionMgrFactory.iExtMgr = extmgr

class LogAnalyzer_StubInjectedViaFactory(object):
    def __init__(self):
        self.mIExtensionMgr = ExtensionMgrFactory.Create()
    
    def IsValidLogFileName(self, fileName):
        self.mIExtensionMgr.IsValid(fileName)
        

#Referred to "2.1 use local virtual factory method to get instance of stub"
class LogAnalyzer_StubInjectedViaLocalFactoryMethod(object):
    def IsValidLogFileName(self, fileName):
        self.GetMgr().IsValid(fileName)
    def GetMgr(self):
        return FileExtensionMgr_ConcreteImpl()

class TestableLogAnalyzer_ReturnStub(LogAnalyzer_StubInjectedViaLocalFactoryMethod):
    def __init__(self, iExtensionMgr):
        self.mIExtensionMgr = iExtensionMgr
    def GetMgr(self):
        return self.mIExtensionMgr


#Referred to "2.2 use extract and override to return a logical result instead of calling an actual denpendency"
class LogAnalyzer_OverrideMethodReturnsResult(object):
    def __init__(self):
        self.mIExtensionMgr =  FileExtensionMgr_ConcreteImpl()
    def IsValidLogFileName(self, fileName):
        self.IsValidExtension(fileName)
    def IsValidExtension(self,filename):
        return self.mIExtensionMgr.IsValid(filename)

class TestableLogAnalyzer_OverrideMethodReturnsResult(LogAnalyzer_OverrideMethodReturnsResult):
    def __init__(self, is_valid_entension):
        self.is_valid_entension = is_valid_entension
    def IsValidExtension(self,filename):
        return self.is_valid_entension



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
        
    # OverrideMethodReturnsResult
    def test_IsValidLogFileName_BadExtension_ReturnFalse_4_OverrideMethodReturnsResult(self):
        is_valid_extension = False
        
        testableLogAnalyzer = TestableLogAnalyzer_OverrideMethodReturnsResult(is_valid_extension)
        ret = testableLogAnalyzer.IsValidLogFileName('fnl.sl')
        
        self.assertFalse(ret)
        
if __name__ == '__main__': 
    unittest.main()