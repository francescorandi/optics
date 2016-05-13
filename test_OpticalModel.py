import OpticalModel, Oscillators
import unittest

class OpticalModelAddTest(unittest.TestCase):
    """Testing the add and addCollection methods in OpticalModel.py."""

    def setUp(self):
        self.om = OpticalModel.OpticalModel()

    def testAddNone(self):
        """Testing adding no oscillator"""
        pass

    def testAddOne(self):
        """Testing adding one oscillator."""
        self.osc1 = Oscillators.Drude(1,1)
        self.om.add(self.osc1)
        self.assertEqual(self.om.oscillators[0], self.osc1)

    # def testAddTwo(self):
    #     """Testing adding two oscillators."""
    #     self.osc1 = Oscillators.Drude(1,1)
    #     self.osc2 = Oscillators.Drude(2,2)
    #     self.om.add(self.osc1, self.osc2)
    #     self.assertIn(self.osc1, self.om.oscillators)
    #     self.assertIn(self.osc2, self.om.oscillators)

    def testAddListEmpty(self):
        """Testing adding a list with no oscillators."""
        self.om.addCollection([])
        self.assertEqual(self.om.oscillators, [])

    def testAddListOne(self):
        """Testing adding a list with one oscillator."""
        self.osc1 = Oscillators.Drude(1,1)
        self.om.addCollection([self.osc1])
        self.assertIn(self.osc1, self.om.oscillators)

    def testAddListTwo(self):
        """Testing adding a list with two oscillators."""
        self.osc1 = Oscillators.Drude(1,1)
        self.osc2 = Oscillators.Drude(2,2)
        self.om.addCollection([self.osc1, self.osc2])
        self.assertIn(self.osc1, self.om.oscillators)
        self.assertIn(self.osc2, self.om.oscillators)

class OpticalModelTest(unittest.TestCase):
    """Testing creation, deletion, __str__, and __repr__."""

    def testConstructionEmpty(self):
        """Indirect test for OpticalModelInstances()"""
        self.om = OpticalModel.OpticalModel()
        self.assertEqual(OpticalModel.OpticalModel.OpticalModelInstances(),1)
        self.assertEqual(self.om.oscillators, [])
        self.assertEqual(self.om.name, "Optical Model 1")

    def test__str__(self):
        pass

    def test__repr__(self):
        pass

class OpticalModelBinaryTest(unittest.TestCase):
    """Testing binary operations."""

    def setUp(self):
        self.om1 = OpticalModel.OpticalModel()
        self.om2 = OpticalModel.OpticalModel()
        self.osc1 = Oscillators.Drude(1,1)
        self.osc2 = Oscillators.Drude(2,2)
        self.om1.add(self.osc1)
        self.om2.add(self.osc2)

    def testAdd(self):
        self.om3 = self.om1 + self.om2
        self.assertIn(self.osc1, self.om3.oscillators)
        self.assertIn(self.osc2, self.om3.oscillators)

    def testAddInplace(self):
        self.om1 += self.om2
        self.assertIn(self.osc1, self.om1.oscillators)
        self.assertIn(self.osc2, self.om1.oscillators)

    def testAddReciprocalSingle(self):
        self.om1 += [self.osc1]
        self.assertIn(self.osc1, self.om1.oscillators)

    def testAddReciprocalList(self):
        self.om1 += [self.osc1, self.osc2]
        self.assertIn(self.osc1, self.om1.oscillators)
        self.assertIn(self.osc2, self.om1.oscillators)

class OpticalModelContainerTest(unittest.TestCase):

    def setUp(self):
        self.om = OpticalModel.OpticalModel()
        self.osc1 = Oscillators.Drude(1,1)
        self.osc2 = Oscillators.Gauss(2,2,2)
        self.om.add(self.osc2)
        self.om.add(self.osc1)

    def testSort(self):
        self.om.sort()
        self.assertListEqual(self.om.oscillators, [self.osc1, self.osc2])

    def testContains(self):
        self.assertTrue(self.osc1 in self.om)

class OpticalModelPropertiesTest(unittest.TestCase):

    def setUp(self):
        self.om = OpticalModel.OpticalModel()
        self.osc1 = Oscillators.Gauss(2,2,2)
        self.om.add(self.osc1)

    def testTotalSpectralWeigth(self):
        raise NotImplementedError

    def testPartialSpectralWeight(self):
        raise NotImplementedError


if __name__ == '__main__':
        unittest.main()
