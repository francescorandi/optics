Optics
======

It is a suite of tools developed in Python3 to deal with optical spectroscopy data in Condensed Matter research. The long term goal is to develop an open source and more flexible replacement to the core aspects of the widely used Reffit software.

The first goal is to develop a framework for oscillator models that it is easy to expand. Implementing Drude, Lorentz and Gauss lineshapes in a standard representation and one alternative one.

Future features include (in no particular order):
- Fitting an oscillator model to a set of data
- Kramers-Kronig calculation
- Workspace-environment save/load
- Processing (unit transformation, smoothing, binning, etc) and manipulation (scale, shift, etc) of datasets
- Fancier oscillator models: tauc, extended lorentz, others

Dependencies
------------

- Python =< 3.4
- numpy =< 1.9.1
- scipy =< 0.14.0
- matplotlib =< 1.4.2
