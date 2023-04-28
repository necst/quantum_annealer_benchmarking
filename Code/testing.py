from setpacking import SetPackingProblem, read_sanitized_file, print_qubits_info
from dwave.embedding import *
from dimod import BinaryQuadraticModel
from dwave.system import DWaveSampler
from dwave.system import LeapHybridSampler
from dwave.system import EmbeddingComposite
from dwave.inspector import *
from dwave.embedding.chimera import *
from dwave.embedding.chain_strength import *
import JSONgenerator
import gc
f = open("strength.csv", "a")
f.write("platform,num,strength\n")
for j in range(9,10):
    f_2000Q = open("Datasets/2000Q_new/try_%d.csv" % j, "a")
    f_adv = open("Datasets/Adv_new/try_%d.csv" % j, "a")
    f_2000Q.write("numvar, minenergy, maxenergy, numqubit, maxchainlength, chainstrength, qpusamplingtime, qpuannealtimepersample, qpureadouttimepersample, qpuaccesstime, qpuaccessoverheadtime, qpuprogrammingtime, qpudelaytimepersample, totalpostprocessingtime, postprocessingoverheadtime\n")
    f_adv.write("numvar, minenergy, maxenergy, numqubit, maxchainlength, chainstrength, qpusamplingtime, qpuannealtimepersample, qpureadouttimepersample, qpuaccesstime, qpuaccessoverheadtime, qpuprogrammingtime, qpudelaytimepersample, totalpostprocessingtime, postprocessingoverheadtime\n")
    for i in range(1,61):
        JSONgenerator.generate('Datasets/temp.json', i)
        problem = read_sanitized_file('Datasets/temp.json')[0]
        sampleset = problem.prepare()
        sampler_2000Q = EmbeddingComposite(DWaveSampler(solver={'topology__type': 'chimera'}))
        chain_strength_2000Q = uniform_torque_compensation(problem.bqm, sampler_2000Q, 2.0)
        sampleset = sampler_2000Q.sample(problem.bqm, chain_strength_2000Q, label="Set Packing", num_reads = 100)
        max_energy = sampleset.first.energy
        for datum in sampleset.data():
            if max_energy < datum.energy:
                max_energy = datum.energy
        embedding = sampleset.info['embedding_context']['embedding']
        lengths = [len(chain) for chain in embedding.values()]
        num_qubit = sum(lengths)
        max_chain_length = max(lengths)
        f_2000Q.write("%d, %f, %f, %d, %d, %f, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % \
            ( i, sampleset.first.energy, max_energy, num_qubit, max_chain_length, chain_strength_2000Q, \
               str(sampleset.info['timing']['qpu_sampling_time']), str(sampleset.info['timing']['qpu_anneal_time_per_sample']), \
               str(sampleset.info['timing']['qpu_readout_time_per_sample']), str(sampleset.info['timing']['qpu_access_time']), \
               str(sampleset.info['timing']['qpu_access_overhead_time']), str(sampleset.info['timing']['qpu_programming_time']), \
               str(sampleset.info['timing']['qpu_delay_time_per_sample']), str(sampleset.info['timing']['total_post_processing_time']), \
             str(sampleset.info['timing']['post_processing_overhead_time']))) 
        
        sampler_adv = EmbeddingComposite(DWaveSampler())
        chain_strength_adv = uniform_torque_compensation(problem.bqm, sampler_adv, 2.0)
        sampleset = sampler_adv.sample(problem.bqm, chain_strength_adv, label="Set Packing", num_reads = 100)
        max_energy = sampleset.first.energy
        for datum in sampleset.data():
            if max_energy < datum.energy:
                max_energy = datum.energy
        embedding = sampleset.info['embedding_context']['embedding']
        lengths = [len(chain) for chain in embedding.values()]
        num_qubit = sum(lengths)
        max_chain_length = max(lengths)
        f_adv.write("%d, %f, %f, %d, %d, %f, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % \
            ( i, sampleset.first.energy, max_energy, num_qubit, max_chain_length, chain_strength_adv, \
               str(sampleset.info['timing']['qpu_sampling_time']), str(sampleset.info['timing']['qpu_anneal_time_per_sample']), \
               str(sampleset.info['timing']['qpu_readout_time_per_sample']), str(sampleset.info['timing']['qpu_access_time']), \
               str(sampleset.info['timing']['qpu_access_overhead_time']), str(sampleset.info['timing']['qpu_programming_time']), \
               str(sampleset.info['timing']['qpu_delay_time_per_sample']), str(sampleset.info['timing']['total_post_processing_time']), \
             str(sampleset.info['timing']['post_processing_overhead_time']))) 
        
        print("%d, %d\n" % (j,i))
        del problem, sampleset, sampler_2000Q, sampler_adv, embedding, lengths
        gc.collect()
    f_2000Q.close()
    f_adv.close()

for j in range(0,10):
    f_adv = open("Datasets/Adv_new/try_%d.csv" % j, "a")
    for i in range(61,150):
        JSONgenerator.generate('Datasets/temp.json', i)
        problem = read_sanitized_file('Datasets/temp.json')[0]
        sampleset = problem.prepare()
        sampler_adv = EmbeddingComposite(DWaveSampler())
        chain_strength_adv = uniform_torque_compensation(problem.bqm, sampler_adv, 2.0)
        sampleset = sampler_adv.sample(problem.bqm, chain_strength_adv, label="Set Packing", num_reads = 100)
        max_energy = sampleset.first.energy
        for datum in sampleset.data():
            if max_energy < datum.energy:
                max_energy = datum.energy
        embedding = sampleset.info['embedding_context']['embedding']
        lengths = [len(chain) for chain in embedding.values()]
        num_qubit = sum(lengths)
        max_chain_length = max(lengths)
        f_adv.write("%d, %f, %f, %d, %d, %f, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % \
            ( i, sampleset.first.energy, max_energy, num_qubit, max_chain_length, chain_strength_adv, \
               str(sampleset.info['timing']['qpu_sampling_time']), str(sampleset.info['timing']['qpu_anneal_time_per_sample']), \
               str(sampleset.info['timing']['qpu_readout_time_per_sample']), str(sampleset.info['timing']['qpu_access_time']), \
               str(sampleset.info['timing']['qpu_access_overhead_time']), str(sampleset.info['timing']['qpu_programming_time']), \
               str(sampleset.info['timing']['qpu_delay_time_per_sample']), str(sampleset.info['timing']['total_post_processing_time']), \
             str(sampleset.info['timing']['post_processing_overhead_time']))) 
        
        print("%d, %d\n" % (j,i))
        del problem, sampler_adv, sampleset, embedding, lengths
        gc.collect()
    f_adv.close()
"""
for i in range(2,151):
    JSONgenerator.generate('Datasets/temp.json', i)
    problem = read_sanitized_file('Datasets/temp.json')[0]
    sampleset = problem.prepare()
    sampler = EmbeddingComposite(DWaveSampler())
    chain_strength = uniform_torque_compensation(problem.bqm, sampler, 2.0)
    f.write("advantage, %d, %f\n" % (i,chain_strength))
    print("advantage, %d, %f\n" % (i,chain_strength))
f.close()
"""
