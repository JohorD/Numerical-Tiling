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



    <h2>Requirements</h2>

    <p>
        This project requires the following software and libraries installed:
    </p>

    <ul>
        <li><span class="texttt">python</span></li>
        <li><span class="texttt">numpy</span></li>
        <li><span class="texttt">matplotlib</span></li>
        <li><span class="texttt">scipy</span></li>
        <li><span class="texttt">pickle</span></li>
        <li><span class="texttt">screen</span> (for running persistent terminal sessions)</li>
        <li>Fortran compiler: <span class="texttt">gfortran</span> or <span class="texttt">ifx</span></li>
    </ul>

    <style>
        .texttt {
            font-family: "Courier New", Courier, monospace;
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 4px;
        }
    </style>

