=====================
YAML to sif converter
=====================

A command line utility that translates ``yaml`` files to ElmerSolver solver input file (``.sif``)

Usage
-----

Top level keys are translated as ``sif`` sections in random order except for following exceptions.

1. String in ``prologue`` is printed verbatim at start of the ``sif`` file as such

2. Section with key matching ``header`` (case insensitive) is printed next.

3. The rest of the keys are are printed in order given in the ``yaml`` file.

3. After other sections, string in ``epilogue`` is printed verbatim.

See examples/esim1.yml.
