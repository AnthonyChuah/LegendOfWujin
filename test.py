class Testclass(object):
	def __init__(self,test1):
		self.test1 = test1

class Testother(object):
	def __init__(self,test1,test2):
		Testclass.__init__(self,test1)
		self.test2 = test2

Testobj = Testclass("test1")
Otherobj = Testother("test1special","test2")
print(Testobj.test1)
print(Otherobj.test1)
print(Otherobj.test2)