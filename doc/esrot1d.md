# esro1d package overview



The **esrot1d** package contains the following modules:



- **baseline.py** :    convenience classes for storing lists of critical d-values and their interpretation labels
- **dec.py** :  decorator classes, mainly to minimize code elsewhere (e.g. function vectorization)
- **io.py** : in/out functions for saving and loading data in HDF5 format;  used for experimental data and simulation results
- **smoothness.py** : functions for estimating functional smoothness and converting between smoothness parameters
- **stats/d.py** : functions for calculating d-values for 1- and 2-sample designs and converting between t- and d-values
- **stats/p.py** : probability calculations including critical d-values given critical p-values
- **util.py** : utility functions for plotting, sorting and printing

