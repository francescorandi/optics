from Oscillators import Drude
import unittest

class DrudeParameterValidationTest(unittest.TestCase):

    def testConstruction(self):
        self.drude = Drude(1,1)
        self.assertEqual(self.drude.amplitude, 1.0)
        self.assertEqual(self.drude.width, 1.0)

    def testConstructionNegative(self):
        self.drude = Drude(-1,-1)
        self.assertEqual(self.drude.amplitude, 0.0)
        self.assertEqual(self.drude.width, 0.0)

if __name__ == '__main__':
        unittest.main()
