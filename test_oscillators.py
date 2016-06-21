from Oscillators import Drude
import unittest


class ParameterValidationTest(unittest.TestCase):

    def testConstructionCorrect(self):
        self.drude = Drude(1, 1)
        self.assertEqual(self.drude.amplitude, 1.0)
        self.assertEqual(self.drude.width, 1.0)

    def testConstructionString(self):
        self.drude = Drude('1', '1')
        self.assertEqual(self.drude.amplitude, 1.0)
        self.assertEqual(self.drude.width, 1.0)

    def testConstructionNegative(self):
        self.drude = Drude(-1, -1)
        self.assertEqual(self.drude.amplitude, 0.0)
        self.assertEqual(self.drude.width, 0.0)

    def testRepresentation(self):
        self.drude = Drude(1, 1)
        self.drudefromrerp = eval(repr(self.drude))
        self.assertNotEqual(self.drude, self.drudefromrerp)

if __name__ == '__main__':
        unittest.main()
