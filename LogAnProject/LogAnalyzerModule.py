#!/usr/bin/env python 
#encoding: utf-8 

# the simplyest way to test return value 
# No needs to use stub
class LogAnalyzer_0(object):
	def IsValidLogFileName(self, fileName):
		return str(fileName).endswith('.sln')

# However, when we have to interact with filesystem in the mut, we have to use
# mock
# eg.  new mut may look like this:
# def IsValidLogFileName(fileName):
# read through the config file and return true if extension is supported in
# config file
# So below are all about using stub of IExtensionMgr
class IExtensionMgr(object):
	def IsValid(self,filename):
		pass

class FileExtensionMgr(object):
	def IsValid(self,filename):
		return str(fileName).endswith('.sln') 

class LogAnalyzer_1(object):
	def __init__(self, iExtensionMgr):
		self.mIExtensionMgr = iExtensionMgr

	def IsValidLogFileName(self, fileName):
		self.mIExtensionMgr.IsValid(fileName)

class LogAnalyzer_2(object):
	def __init__(self):
		self.mIExtensionMgr = FileExtensionMgr()

	def IsValidLogFileName(self, fileName):
		self.mIExtensionMgr.IsValid(fileName)

	def SetIExtensionMgr(self, ext):
		self.mIExtensionMgr = ext

class ExtensionMgrFactory(object):
	iExtMgr = None

	@staticmethod
	def Create():
		if ExtensionMgrFactory.iExtMgr is None:
			ExtensionMgrFactory.iExtMgr = FileExtensionMgr()
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
