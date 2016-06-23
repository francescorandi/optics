# -*- coding: utf-8 -*-

"""
Utilities to handle models created with J.A. Woollam WVase Genosc.
"""

import csv

from OpticalModel import *
from Oscillators import *


class GenoscModel:
    """A particular Genosc model representation class.
    Imports a Genosc model file """

    def __init__(self, filename, name=None, desc=None):

        self.name = name
        self.desc = desc
        self.oscillators = []
        self.einf = None

        with open(filename, 'r') as f:
            reader = csv.reader(f)
            self.commentary = next(reader)[0]
            _tmp = next(reader)[0]
            if _tmp != 'GENOSC':
                raise TypeError
            next(reader)  # Skipping row indicating number of oscillators and other info
            eps1 = next(reader)[0]  # Getting epsilon 1 extra info
            self.einf = eps1[0]
            next(reader)  # Getting rid of the energy range line
            try:
                # Reading the oscillators
                for row in reader:
                    row = row[0].split()
                    if row[1] == '0':
                        self.oscillators.append(Lorentz(row[3], row[4], row[5]))
                    elif row[1] == '2':
                        self.oscillators.append(Gauss(row[3], row[4], row[5]))
                    elif row[1] == '6':
                        self.oscillators.append(Drude(row[3], row[4]))
            except csv.Error as e:
                print('file %s, line %d: %s' % (filename, reader.line_num, e))

    def t(self):
        _om = OpticalModel(name=self.name, desc=self.desc, oscillators=self.oscillators)
        _om.einf = self.einf
        return _om