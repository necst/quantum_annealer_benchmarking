# On the Design and Characterization of Set Packing Problem on Quantum Annealers

This repository contains source code and dataset for the work "On the Design and Characterization of Set Packing Problem on Quantum Annealers", published at IEEE Eurocon 2023. 
This work presents a solver for Set Packing Problem on quantum annealers exploiting the QUBO model. We
introduce a general format to express instances of the Set Packing Problem that enables an automatic characterization, lowering the barriers to adopting quantum annealers. Finally, we compare the performance of two quantum annealer on the Set Packing, namely D-Wave 2000Q and Advantage, highlighting their pros and cons.

In folder Code, there is the source code of the software. In particular, file setpacking.py contains the necessary tools to create an instance of Set Packing Problem to solve by using D-Wave quantum annealers 2000Q and Advantage. File JSONgenerator.py contains the utility to generate random instances of Set Packing Problems, according to the presented format.

In folder Datasets, it is possible to observe examples of experiments run on D-Wave quantum annealers 2000Q and Advantage, in which, for each specific size of problem, the minimum and maximum energy of the solutions and the execution time is shown.
Additionally, two example of input files, following our proposed format, are shown.

### Creditors and Contributors
Contributors: Venere, Marco and Sorrentino, Giuseppe and Branchini, Beatrice and Conficconi, Davide and Di Nitto, Elisabetta and Sciuto, Donatella and Santambrogio, Marco D.

If you find this repository useful, please use the following citation:


```
@inproceedings{venere2023onthedesign,
  title={On the Design and Characterization of Set Packing Problem on Quantum Annealers},
  author={Venere, Marco and Giuseppe, Sorrentino and Branchini, Beatrice and Conficconi, Davide and Di Nitto, Elisabetta and Sciuto, Donatella and Santambrogio, Marco},
  booktitle={IEEE EUROCON 2023 International Conference on Smart Technologies},
  year={2023}
}

```
