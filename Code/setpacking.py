from dimod import BinaryQuadraticModel
from dwave.system import DWaveSampler
from dwave.system import LeapHybridSampler
from dwave.system import EmbeddingComposite
from dwave.inspector import *
from dwave.embedding.chimera import *
from dwave.embedding.chain_strength import *
import json
import JSONgenerator

class SetPackingProblem:
    """This class represents a set-packing problem, 
    in which set elements must be inserted into n different subsets, 
    such that each element is inserted in at most one subset.
    If differents weights are associated to each subset, the goal is to achieve
    a subsets selection of maximum weight. """
    def __init__(self, subsets, weights, constraints): 
        """This is the constructor of the SetPackingProblem class.
        Params:
        sets_number: number of possible subsets
        weights: weight associated to each different subset.
            Defaults weights are unitary for each subset.
        constraints: a list of sets_number constraints.""" 
        self.s = subsets 
        if weights == None:
            weights = [1] * len(subsets)
        self.w = weights
        self.c = constraints

    def prepare(self):
        """This method solves this problem by using the BQM API of D-Wave Leap.
            Returns a dictionary in which subsets are the key of the dictionary, and their
            corresponding value is 1 if that subset is selected, 0 otherwise."""
        self.bqm = BinaryQuadraticModel({}, {}, 0, 'BINARY')
        for i in range(len(self.s)):
            self.bqm.offset += 1
            self.bqm.add_variable(self.s[i], 0-(self.w[i])) #add variable for subset
        for cons in self.c:
            for i in range(len(cons)):
                for j in range(i):
                    self.bqm.add_interaction(cons[i], cons[j], 6) #add constraint to avoid two non-disjoint subsets being selected       
        return self

    def sample_hybrid(self):
        """
            This method does the sampling of this problem, by using the LeapHybridSampler.
            It must be called after the prepare() method."""
        sampler = LeapHybridSampler(solver={'category': 'hybrid'})
        sampleset = sampler.sample(self.bqm, label="Set Packing")
        return sampleset
    
    def sample_composite(self, show_inspector = False, pre_factor = 2.0, num_of_reads = 100):
        """
            This method does the sampling of this problem, by using the 2000Q platform and DWaveSampler.
            It must be called after the prepare() method.
            Params:
                show_inspector: boolean, if set to True the inspector screen is shown;
                pre_factor: a parameter required by the function used to set the chain strength for the sampling;
                num_of_reads: number of samples asked to the solver.
                """
        sampler = EmbeddingComposite(DWaveSampler(solver={'topology__type': 'chimera'}))
        chain_strength = uniform_torque_compensation(self.bqm, sampler, pre_factor)
        sampleset = sampler.sample(self.bqm, chain_strength, label="Set Packing", num_reads = num_of_reads)
        if show_inspector:
            show(sampleset) 
        return sampleset
    
    def sample_advantage(self, show_inspector = False, pre_factor = 2.0, num_of_reads = 100):
        """
            This method does the sampling of this problem, by using the Advantage platform and DWaveSampler.
            It must be called after the prepare() method.
            Params:
                show_inspector: boolean, if set to True the inspector screen is shown;
                pre_factor: a parameter required by the function used to set the chain strength for the sampling;
                num_of_reads: number of samples asked to the solver."""
        sampler = EmbeddingComposite(DWaveSampler())
        chain_strength = uniform_torque_compensation(self.bqm, sampler, pre_factor)
        sampleset = sampler.sample(self.bqm, chain_strength, label="Set Packing", num_reads = num_of_reads)
        if show_inspector:
            show(sampleset) 
        return sampleset

def read_sanitized_file(filename):
    """
    This method receives input from a file, verifies if it is consistent and constructs a list of instances of the class SetPackingProblem.
    Returns a list of instances of the class SetPackingProblem, if problems are correctly inserted.
    Throws a ValueError exception if data type is not consistent.
    Throws a json.decoder.JSONDecodeError exception if file is not correctly encoded.
    """
    with open(filename, "r") as f:
        data = json.load(f)
        problems = []
        for problem in data:
            subsets = problem["subsets"]
            sets = []
            weights = []
            for set in subsets:
                sets.append(set["name"])
                if "weight" in set:
                    try:
                        weights.append(int(set["weight"]))
                    except ValueError:
                        print("Weight attribute must be integer")
                        exit()
                else:
                    weights.append(1)
                for i in range(len(sets)):
                        for j in range(i):
                            if(sets[i] == sets[j]):
                                print("Identifier already inserted in subsets list")
                                exit()
            constraints = problem["constraints"]
            c = []
            for cons in constraints:
                c.append(cons["sets"])
                for elem in cons["sets"]:
                    if elem not in sets:
                        print("Undefined subsets")
                        exit()
                for i in range(len(cons["sets"])):
                    for j in range(i):
                        if(cons["sets"][i] == cons["sets"][j]):
                            print("Identifier already inserted in this constraint")
                            exit()
        problems.append(SetPackingProblem(sets, weights, c))
    return problems

def get_sanitized_input():
    """This method receives input from the user, verifies if it is consistent and constructs an instance of the class SetPackingProblem.
    Returns an instance of the class SetPackingProblem, if problem is correctly inserted.
    Throws a ValueError exception otherwise."""
    while True:
        print("Insert the number of the subsets: ")
        n = input()
        try:
            n = int(n)
            if n < 0:
                raise ValueError("A positive integer number must be inserted")
            subsets = []
            for i in range(n):
                print("Insert one-character identifier for element: ", i + 1)
                value = input()
                if(len(value) > 1):
                    raise ValueError("Identifiers must have only one character")
                if value in subsets:
                    raise ValueError("Identifier already inserted")
                subsets += value
            print("Do you wish to insert weights for subsets? Y/N")
            ans = input()
            try:
                weights = []
                if ans == "Y" or ans == "y":
                    for i in range(n):
                        print("Insert numeric weight for subset: ", subsets[i])
                        value = input()
                        value = int(value)
                        weights.append(value)
                elif ans == "N" or ans == "n":
                    weights = None
                else:
                    raise TypeError("Only Y/y or N/n are acceptable answers.")
                print("Insert the number of the constraints: ")
                m = input()
                try:
                    m = int(m)
                except ValueError:
                    print("A positive integer number must be inserted")
                    continue
                if m < 0: 
                    raise ValueError("A positive integer number must be inserted")
                constraints = []
                for i in range(m):
                    print("Insert the number of subsets for constraint #{}:".format(i+1))
                    num = input()
                    num = int(num)
                    if num < 0:
                        raise ValueError("A positive integer number must be inserted")
                    c = []
                    print("Insert elements:")
                    for i in range(num):
                        c1 = input()
                        if c1 in c:
                            raise ValueError("Identifier already inserted in this constraint")
                        c += c1
                        if c[i] not in subsets:
                            raise ValueError("Identifier not valid.")
                    constraints.append(c)
                return SetPackingProblem(subsets, weights, constraints)
            except TypeError as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                continue
        except ValueError as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            continue

def test_comp(comp_prefix, num_files = 10):
    """
        This method does testing for the 2000Q platform. 
        It runs num_files experiments, for each of which it prints out the result on a separate file.
        Each experiment generates random problems with N subsets varying from 1 up to 60 included.
        Params:
            comp_prefix: prefix of file names, to which an increment number is added;
            num_files: number of files to print (and thus, number of experiments to run)."""
    for j in range(num_files):
        for i in range(1, 61, 1):
            with open(f'{comp_prefix}{j+1}.txt', 'a') as f:
                JSONGenerator.generate('Datasets/temp.json', i)
                problem = read_sanitized_file('Datasets/temp.json')[0]
                sampleset = problem.prepare().sample_composite(pre_factor = 2.0, num_of_reads = 100)
                max_energy = sampleset.first.energy
                for datum in sampleset.data():
                    if max_energy < datum.energy:
                        max_energy = datum.energy
                f.write(f"{i}: min_energy: {sampleset.first.energy}, max_energy: {max_energy}, {str(sampleset.info['timing'])}\n")
                print(f"file composite #{j+1}, step #{i}")
            f.close()

def test_adv(adv_prefix, num_files = 10):
    """
        This method does testing for the Advantage platform. 
        It runs num_files experiments, for each of which it prints out the result on a separate file.
        Each experiment generates random problems with N subsets varying from 1 up to 150 included.
        Params:
            adv_prefix: prefix of file names, to which an increment number is added;
            num_files: number of files to print (and thus, number of experiments to run)."""
    for j in range(num_files):
        for i in range(1, 151, 1):
            with open(f'{adv_prefix}{j+1}.txt', 'a') as f:
                JSONGenerator.generate('Datasets/temp.json', i)
                problem = read_sanitized_file('Datasets/temp.json')[0]
                sampleset = problem.prepare().sample_advantage(pre_factor = 2.0, num_of_reads = 100)
                max_energy = sampleset.first.energy
                for datum in sampleset.data():
                    if max_energy < datum.energy:
                        max_energy = datum.energy
                f.write(f"{i}: min_energy: {sampleset.first.energy}, max_energy: {max_energy}, {str(sampleset.info['timing'])}\n")
                print(f"file advantage #{j+1}, step #{i}")
            f.close()

def test_comp_and_adv(comp_prefix, adv_prefix, num_files = 10):
    """
        This method does testing for the 2000Q AND Advantage platform. 
        It runs num_files experiments for both platforms, and for each experiment it prints out the result on a separate file.
        Each experiment generates random problems with N subsets varying from 1 up to 60 included (for 2000Q) and up to 150 included (for Advantage).
        Params:
            comp_prefix: prefix of file names for 2000Q, to which an increment number is added;
            adv_prefix: prefix of file names for Advantage, to which an increment number is added;
            num_files: number of files to print (and thus, number of experiments to run for each platform)."""
    test_comp(comp_prefix, num_files)
    test_adv(adv_prefix, num_files)

def print_qubits_info(sampleset):
    """
        This method prints out number of logical variables and number of physical qubits used in embedding for the given sampleset.
        Params: 
            sampleset: the sampleset for which to print out qubits info"""
    embedding = sampleset.info['embedding_context']['embedding']
    print(f"Number of logical variables: {len(embedding.keys())}")
    print(f"Number of physical qubits used in embedding: {sum(len(chain) for chain in embedding.values())}")
    print(f"Maximum chain length: {max(len(chain) for chain in embedding.values())}")
"""
#USAGE EXAMPLES:

JSONgenerator.generate('Datasets/temp.json', 20)
problem = read_sanitized_file('Datasets/temp.json')[0]
sampleset = problem.prepare().sample_advantage(pre_factor = 2.0, num_of_reads = 100)
print_qubits_info(sampleset)

#test_comp(comp_prefix = 'Datasets/Composite/try', num_files = 1)
#test_adv(adv_prefix = 'Datasets/Advantage/try_', num_files = 3)       

test_comp_and_adv(comp_prefix = 'Datasets/Composite/try_', \
                    adv_prefix = 'Datasets/Advantage/try_', \
                    num_files = 10)


for i in range(1, 160, 1):
    JSONgenerator.generate('data.json', i)
    problem = read_sanitized_file('data.json')[0]
    if(i <= 65):
        with open('2000Q_test.txt', 'a') as q:
            sampleset = problem.prepare().sample_composite()
            q.write(f"{i}: {str(sampleset.info['timing'])}\n")
            q.close()
    with open('Advantage_test.txt', 'a') as a:
        sampleset = problem.prepare().sample_advantage()
        a.write(f"{i}: {str(sampleset.info['timing'])}\n")
        a.close()

#JSONgenerator.generate('Datasets/dataComposite.json',150 )

problem = read_sanitized_file('Datasets/dataComposite.json')[0]
sampleset = problem.prepare().sample_composite(True)

max = sampleset.first.energy
for datum in sampleset.data():
    if max < datum.energy:
        max = datum.energy
print(f"energy = {sampleset.last.energy}")

problem = read_sanitized_file('Datasets/dataComposite.json')[0]
sampleset = problem.prepare().sample_composite(True)
print(str(sampleset.info['timing']))
"""
