import VMserver
import unittest

class TestVMserver(unittest.TestCase):

    def setUp(self):
        self.tested_VMserver = VMserver.VMserver()
        self.name_tested_vm = 'Ubuntu for testing'
        
    def test_start_vm(self):
        self.tested_VMserver.start_vm(self.name_tested_vm)
        self.tested_VMserver.execute()
        self.test_result = self.tested_VMserver.get_statusoutput()
        self.assertEqual(self.test_result[0], 0)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVMserver)
    unittest.TextTestRunner(verbosity=2).run(suite)
