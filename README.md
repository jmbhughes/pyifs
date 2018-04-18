![example IFS](https://raw.githubusercontent.com/jtauber/pyifs/master/example.png)

An Iterated Function System in Python
=====================================

This is a fork of [James Tauber's](https://github.com/jtauber/pyifs) initial work. 

The tone-mapped image handling comes from Minilight.

NOTE: I strongly recommend using PyPy to run this (it runs about 40x faster)

Running
-------

Just run

    python pyifs.py [configuration file]
    

Configuration
-------------

The iterated function system is customizable by using a json configure file ([example](configs/sierpinski.json)).

Writing New Transforms
----------------------

A new subclass of `Transform` should randomize its parameters in `__init__`
then implement a `transform` method that takes two args (the x, y of the
point) and returns a new x, y.


To-do
-----

- let evaluation of iterated function system be multithreaded
- Check on why fern is not centered
- Allow customization of image output (background, color schemes)
- Make an easier input method? graphical? 
- add deterministic mode and allow for viewing of iterated steps

Examples
--------


![example IFS2](https://raw.githubusercontent.com/jtauber/pyifs/master/example2.png)
![example IFS3](https://raw.githubusercontent.com/jtauber/pyifs/master/example3.png)
![example IFS4](https://raw.githubusercontent.com/jtauber/pyifs/master/example4.png)
