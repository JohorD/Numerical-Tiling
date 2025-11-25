<h1 style="font-size: 60px; text-align: center;">
Numerical tiling-based simulations <br>
of decoherence in multifield models of inflation
</h1>

This repository contains the core code required to reproduce the results presented in the paper “Numerical Tiling-Based Simulations of Decoherence in Multifield Models of Inflation.” The routines are designed to be user-friendly and provide a guided tutorial that walks users through our results and enables further exploration of different configurations of decoherence events. 

<p align="center">
  <a href="https://arxiv.org/abs/2511.16801">
    <img src="https://img.shields.io/badge/arXiv-2511.16801-b31b1b.svg" width="200">
  </a>
</p>

The code computes the two-point mode correlation functions (and other observables derived from them) for one and two-field models of inflation, but is easily scalable to theories with an arbitrarily large number of fields.

<p align="center">
  <img src="Movies/mf_wgnr.gif" width="900">
</p>


<h3>Prerequisites</h3>

This project requires the following software:

1. Python environment:
   - <span class="texttt">Python&nbsp;3.9+</span>
   - External Python packages:
     - <span class="texttt">NumPy</span>
     - <span class="texttt">Matplotlib</span>
     - <span class="texttt">Pillow</span>

2. Fortran compiler

   A Fortran compiler is required to build and run the numerical simulations.

   You may use:
   - <span class="texttt">gfortran</span> (GNU Fortran, recommended for portability)
   - <span class="texttt">ifx</span> (for Linux distributions: Intel oneAPI Fortran compiler, recommended for performance)

3. <span class="texttt">screen</span> for persistent terminal sessions

   Some long simulations rely on screen to keep processes running after closing the terminal.


<h3>Modules</h3>


- [<img src="https://img.shields.io/badge/architecture.py-paper-green" height="20">](https://github.com/JohorD/Numerical-Tiling/blob/main/Numerical-Tiling-DEMO-USER/modules_py/architecture.py) :
  - Generates all required directories and files containing data, Fortran source code, and executables. It manages the configuration of decoherence events and the accident-free scenario, which determines the relevant physical scales in the problem. Its behavior depends on the operation mode (single-field or multifield).  
    **Note:** this module and `generate_fortran.py` must be extended to support more than two fields.

- [<img src="https://img.shields.io/badge/configurations.py-paper-green" height="20">](https://github.com/JohorD/Numerical-Tiling/blob/main/Numerical-Tiling-DEMO-USER/modules_py/configurations.py) :
  - Uses the physical scales associated with the accident-free scenario to load the event distribution into the evolution routines, identifying which decoherence events effectively modify the mode dynamics. It also generates a preview of the tile layout used in the mode-injection scheme.

- [<img src="https://img.shields.io/badge/generate_fortran.py-paper-green" height="20">](https://github.com/JohorD/Numerical-Tiling/blob/main/Numerical-Tiling-DEMO-USER/modules_py/generate_fortran.py) :
  - Defines the number of cases to simulate. The user specifies the number of modes and may distribute the workload across multiple parallel processes. This module also sets the location of the physical scale and the sampling rate used when writing evolution data to disk.  
    The number of fields can be adjusted by providing the potential derivatives, the environment operators, and the initial conditions associated with each field.  
    By default, it is prepared to simulate one- and two-field quartic models and allows the use of linear combinations of adiabatic and isocurvature environment operators.

- [<img src="https://img.shields.io/badge/run_fortran.py-paper-green" height="20">](https://github.com/JohorD/Numerical-Tiling/blob/main/Numerical-Tiling-DEMO-USER/modules_py/run_fortran.py) :
  - Compiles and executes the generated Fortran simulations, managing the full execution pipeline.

- [<img src="https://img.shields.io/badge/load_data.py-paper-green" height="20">](https://github.com/JohorD/Numerical-Tiling/blob/main/Numerical-Tiling-DEMO-USER/modules_py/load_data.py) :
  - Provides a dictionary that maps the variables produced by the Fortran code to Python structures. It enables loading and plotting of additional observables such as state purity, entanglement entropy, and related quantities.

- [<img src="https://img.shields.io/badge/styles_format.py-paper-green" height="20">](https://github.com/JohorD/Numerical-Tiling/blob/main/Numerical-Tiling-DEMO-USER/modules_py/styles_format.py) :
  - Defines the plotting style for labels and tick marks, sets scientific notation, and enables TeX rendering for publication-quality figures.
 
<h3>Tutorial</h3>

[<img src="https://img.shields.io/badge/DEMO-TUTORIAL-paper-orange" height="20">](https://github.com/JohorD/Numerical-Tiling/blob/main/Numerical-Tiling-DEMO-USER/Numerical-Tiling-DEMO-USER.ipynb)

<h3>Q&A</h3>
Please report bugs, questions and further improvements to 
<a href="https://mail.google.com/mail/?view=cm&fs=1&to=jpenalbaq@uni.pe" target="_blank">
    jpenalbaq@uni.pe
</a>

