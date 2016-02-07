import OpticalModel, Oscillators.Drude
import unittest

class OpticalModelAddTest(unittest.TestCase):
    """Testing the add method in OpticalModel.py."""

    def testAddNone(self):
        """Testing adding no oscillator"""
        pass

    def testAddOne(self):
        """Testing adding one oscillator."""
        om = OpticalModel.OpticalModel()
        osc1 = Oscillators.Drude.Drude(1,1)
        self.assertEqual(om.oscillators[0], osc1)

    def testAddTwo(self):
        """Testing adding two oscillators."""
        om = OpticalModel.OpticalModel()
        osc1 = Oscillators.Drude.Drude(1,1)
        osc2 = Oscillators.Drude.Drude(2,2)
        om.add(osc1, osc2)
        self.assertIn(osc1, om.oscillators)
        self.assertIn(osc2, om.oscillators)

    def testAddListOne(self):
        """Testing adding a list with one oscillator."""
        om = OpticalModel.OpticalModel()
        osc1 = Oscillators.Drude.Drude(1,1)
        om.add([osc1])
        self.assertIn(osc1, om.oscillators)

    def testAddListTwo(self):
        """Testing adding a list with two oscillators."""
        om = OpticalModel.OpticalModel()
        osc1 = Oscillators.Drude.Drude(1,1)
        osc2 = Oscillators.Drude.Drude(2,2)
        om.add([osc1, osc2])
        self.assertIn(osc1, om.oscillators)
        self.assertIn(osc2, om.oscillators)

    def testAddListThree(self):
        """Testing adding a list with three oscillators."""
        om = OpticalModel.OpticalModel()
        osc1 = Oscillators.Drude.Drude(1,1)
        osc2 = Oscillators.Drude.Drude(2,2)
        osc3 = Oscillators.Drude.Drude(3,3)
        om.add([osc1, osc2, osc3])
        self.assertIn(osc1, om.oscillators)
        self.assertIn(osc2, om.oscillators)
        self.assertIn(osc3, om.oscillators)

if __name__ == '__main__':
        unittest.main()
