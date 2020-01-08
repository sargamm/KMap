import unittest
from HW2_2018262 import minFunc



class testpoint(unittest.TestCase):
	def test_minFunc(self):
		minFunc(3,'(1,2,5,6,7) d (0,3,4)')
		minFunc(1,'(0) d -')
		minFunc(2,'(0,2) d (3)')
		minFunc(4,'(1,3,4,5,7,10,13,15) d (0,2,14)')
		minFunc(3,'(0,2,4,5) d -')
                
if __name__=='__main__':
	unittest.main()
