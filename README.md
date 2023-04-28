# On the Design and Characterization of Set Packing Problem on Quantum Annealers

This repository contains source code and dataset for the work "On the Design and Characterization of Set Packing Problem on Quantum Annealers", published at IEEE EUROCON 2023. 
This work presents a solver for Set Packing Problem on quantum annealers exploiting the QUBO model.
We introduce a general format to express instances of the Set Packing Problem that enables an automatic characterization, lowering the barriers to adopting quantum annealers.
Finally, we compare the performance of two quantum annealer on the Set Packing, namely D-Wave 2000Q and Advantage, highlighting their pros and cons.

In folder `Code`, there is the source code of the software. 
In particular, file `setpacking.py` contains the necessary tools to create an instance of Set Packing Problem to solve by using D-Wave quantum annealers 2000Q and Advantage.
Differently, `JSONgenerator.py` contains the utility to generate random instances of Set Packing Problems, according to the presented format.

In folder `Datasets`, it is possible to observe examples of experiments run on D-Wave quantum annealers 2000Q and Advantage, in which, for each specific size of problem, the minimum and maximum energy of the solutions and the execution time is shown.
Additionally, two example of input files, following our proposed format, are shown.

### Usage example
Following usage examples can be executed on D-Wave Leap IDE.

Example of generation of a random instance of Set Packing Problem, for n = 20, and print of statistical data of output after execution on D-Wave Advantage.
```
from setpacking import SetPackingProblem, read_sanitized_file, print_qubits_info
import JSONgenerator

JSONgenerator.generate('Datasets/temp.json', 20)
problem = read_sanitized_file('Datasets/temp.json')[0]
sampleset = problem.prepare().sample_advantage(pre_factor = 2.0, num_of_reads = 100)
print_qubits_info(sampleset)
```
Example of comparison on D-Wave 2000Q and Advantage, by running 10 different experiments, for several values of n, saved on files.
```
from setpacking import test_comp_and_adv

test_comp_and_adv(comp_prefix = 'Datasets/2000Q/try_', \
                    adv_prefix = 'Datasets/Advantage/try_', \
                    num_files = 10)
```
Additional testing can be run by using:
```
python3 Code/testing.py
```

### Creditors and Contributors
Contributors:  Marco Venere, Giuseppe Sorrentino, Beatrice Branchini, Davide Conficconi, Elisabetta Di Nitto, Donatella Sciuto, Marco D. Santambrogio.

If you find this repository useful, please use the following citation:


```
@inproceedings{venere2023onthedesign,
  title={On the Design and Characterization of Set Packing Problem on Quantum Annealers},
  author={Venere, Marco and Sorrentino, Giuseppe and Branchini, Beatrice and Conficconi, Davide and Di Nitto, Elisabetta and Sciuto, Donatella and Santambrogio, Marco D},
  booktitle={IEEE EUROCON 2023 International Conference on Smart Technologies},
  year={2023}
}

```
