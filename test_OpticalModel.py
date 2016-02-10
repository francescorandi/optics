import OpticalModel, Oscillators.Drude
import unittest

class OpticalModelAddTest(unittest.TestCase):
    """Testing the add and addCollection methods in OpticalModel.py."""

    def setUp(self)::
        om = OpticalModel.OpticalModel()

    def testAddNone(self):
        """Testing adding no oscillator"""
        pass

    def testAddOne(self):
        """Testing adding one oscillator."""
        osc1 = Oscillators.Drude.Drude(1,1)
        om.add(osc1)
        self.assertEqual(om.oscillators[0], osc1)

    def testAddTwo(self):
        """Testing adding two oscillators."""
        osc1 = Oscillators.Drude.Drude(1,1)
        osc2 = Oscillators.Drude.Drude(2,2)
        om.addCollection(osc1, osc2)
        self.assertIn(osc1, om.oscillators)
        self.assertIn(osc2, om.oscillators)

    def testAddListEmpty(self):
        """Testing adding a list with no oscillators."""
        om.addCollection([])
        self.assertEqual(om.oscillators, [])

    def testAddListOne(self):
        """Testing adding a list with one oscillator."""
        osc1 = Oscillators.Drude.Drude(1,1)
        om.addCollection([osc1])
        self.assertIn(osc1, om.oscillators)

    def testAddListTwo(self):
        """Testing adding a list with two oscillators."""
        osc1 = Oscillators.Drude.Drude(1,1)
        osc2 = Oscillators.Drude.Drude(2,2)
        om.addCollection([osc1, osc2])
        self.assertIn(osc1, om.oscillators)
        self.assertIn(osc2, om.oscillators)

class OpticalModelTest(unittest.TestCase):
    """Testing creation, deletion, __str__, and __repr__."""

    def testConstructionEmpty(self):
        """Indirect test for OpticalModelInstances()"""
        om = OpticalModel.OpticalModel()
        self.assertEqual(OpticalModel.OpticalModel.OpticalModelInstances(),1)
        self.assertEqual(om.oscillators, [])
        self.assertEqual(self.om.name, "Optical model 1")

    def test__str__(self):
        pass

    def test__repr__(self):
        pass

class OpticalModelBinaryTest(unittest.TestCase):
    """Testing binary operations."""

    def setUp(self):
        om1 = OpticalModel.OpticalModel()
        om2 = OpticalModel.OpticalModel()
        osc1 = Oscillators.Drude.Drude(1,1)
        osc2 = Oscillators.Drude.Drude(2,2)
        om1.add(osc1)
        om2.add(osc2)

    def testAdd(self):
        om3 = om1 + om2
        self.assertIn(osc1, om3.oscillators)
        self.assertIn(osc2, om3.oscillators)

    def testAddInplace(self):
        om1 += om2
        self.assertIn(osc1, om1.oscillators)
        self.assertIn(osc2, om1.oscillators)

    def testAddReciprocalSingle(self):
        pass

    def testAddReciprocalList(self):
        pass

if __name__ == '__main__':
        unittest.main()
