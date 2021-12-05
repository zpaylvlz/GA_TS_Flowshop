import numpy as np

file1 = open('20x5data.txt','r')
count = 0
machine = 5
job = 0
seed = 0
job_seq = []


def Initial_population():
    population = []
    np.random.seed(seed)
    for i in range(100):
        population.append(np.random.permutation(range(0, job)))
    return list(population)

def Partial_Opposed_based(p):
    bestidx = 0
    min_makespan = 1000000
    for i in range(100):
        temp = Makespan(p[i], job // 2)
        if (temp < min_makespan):
            min_makespan = temp
            bestidx = i
    for i in range(100):
        temp1 = list(p[i].copy())
        partial_left = list(p[bestidx].copy())
        for j in range (job // 2):
            temp1.remove(partial_left[j])
        partial_left.extend(temp1)
        p[i] = []
        p[i].extend(partial_left[:job//2])
        p[i].extend(temp1)
    return p

def Select_Tourment():
    return

def Mutation():
    return
    
def Makespan(ch_job, job_size):
    #print(ch_job)
    makespan_sumup = []
    for i in range (machine):
        temp = []
        makespan_sumup.append(temp)
    for j in range(job_size):
        for i in range(machine):
            if (j == 0):
                makespan_sumup[i].append(job_seq[i][ch_job[0]])
            else:
                if (i == 0):
                    makespan_sumup[i].append(makespan_sumup[i][j-1]+job_seq[i][ch_job[j]])
                else:
                    makespan_sumup[i].append(max(makespan_sumup[i-1][j], makespan_sumup[i][j-1]) + job_seq[i][ch_job[j]])
    return makespan_sumup[machine - 1][job_size - 1]

def Crossover():
    return

while True:
    line = file1.readline()
    if not line:
        break
    count += 1
    if (count == 2):
        split_val = line.split()
        job = int(split_val[0])
        machine = int(split_val[1])
        seed = int(split_val[2])
        population = Initial_population()
    elif (count >= 4):
        split_val = line.split()
        split_val = list(map(int, split_val))
        job_seq.append(split_val)
    if (count == machine + 3):
        count = 0
        Partial_Population = Partial_Opposed_based(population)
        for i in range (100):
            print (Partial_Population[i])
        job_seq = []
file1.close()
a= input()
