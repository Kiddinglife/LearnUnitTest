#!/usr/bin/env python 
#encoding: utf-8 

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
1.Test are performed on the MUT itself
	1.1 Abstracting concrete objects into interfaces or delegates
		How: Extract an interface to allow replacing or extending underlying impl
	1.2 Refactoring to allow injection of faked implementations of those delegates or interface.
		How: 
		1.2.1.Inject stub impl into a class under test (bad as mixup src and test codes)
		1.2.2.Inject stub impl via ctor (cumbersome whenyou have many dependencies)
		1.2.3.Inject stub impl via setter/getter
		  	  this is much simpler than ctor injection as each test can set only the dependencies
		  	  that it needs to get the test underway.
		1.2.4.Inject stub impl via parameter
2.Test are performed on the class that inhetites from MUT
	2.1 
"""

#Refered to "1.1 Abstracting concrete objects into interfaces or delegates"
class ExtensionMgr_AbstractedInterface(object):
	def IsValid(self, filename):  # should be overwriten by child 
		pass

class FileExtensionMgr_ConcreteImpl(ExtensionMgr_AbstractedInterface):
	def IsValid(self, filename): 
		return str(filename).endswith('.sln') 
	

class ExtendMgr_StubIjectedViaCtor(ExtensionMgr_AbstractedInterface):
    def __init__(self):
        self.mWillBeValid = False
        return ExtensionMgr_AbstractedInterface.__init__(self)

    def IsValid(self, filename):
        return self.mWillBeValid

class StubIjectedViaCtor_WithoutIngeritingFrom_ExtensionMgr_AbstractedInterface(object):
    def __init__(self):
        self.mWillBeValid = False

    def IsValid(self, filename):
        return self.mWillBeValid
      
#Refered to 1.2.2.Inject stub impl via ctor (cumbersome whenyou have many dependencies) 
class LogAnalyzer_StubInjectedViaCtor(object):
	def __init__(self, iExtensionMgr):
		self.mIExtensionMgr = iExtensionMgr

	def IsValidLogFileName(self, fileName):

		self.mIExtensionMgr.IsValid(fileName)
		
#Refered to "1.2.3.Inject stub impl via a setter"
class LogAnalyzer_2(object):
	def __init__(self):
		self.mIExtensionMgr = FileExtensionMgr_ConcreteImpl()

	def IsValidLogFileName(self, fileName):
		self.mIExtensionMgr.IsValid(fileName)

	def SetIExtensionMgr(self, ext):
		self.mIExtensionMgr = ext

class ExtensionMgrFactory(object):
	iExtMgr = None

	@staticmethod
	def Create():
		if ExtensionMgrFactory.iExtMgr is None:
			ExtensionMgrFactory.iExtMgr = FileExtensionMgr_ConcreteImpl()
		else:
			return ExtensionMgrFactory.iExtMgr

	@staticmethod
	def SetExtMgr(extmgr):
		ExtensionMgrFactory.iExtMgr = extmgr

class LogAnalyzer_3(object):
	def __init__(self):
		self.mIExtensionMgr = ExtensionMgrFactory.Create()
	
	def IsValidLogFileName(self, fileName):
		self.mIExtensionMgr.IsValid(fileName)
