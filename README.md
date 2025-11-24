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
   - <span class="texttt">ifx</span> (Intel oneAPI Fortran compiler, recommended for performance)

3. <span class="texttt">screen</span> for persistent terminal sessions

   Some long simulations rely on screen to keep processes running after closing the terminal.


<h3>Modules</h3>

1. styles_format.py:
   -
2. architecture.py:
   -
3. generate_fortran.py:
   -
4. run_fortran.py:
   -
5. load_data.py:
   -
6. configurations.py:
   -




