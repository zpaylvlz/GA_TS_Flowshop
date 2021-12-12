import numpy as np
import time
import matplotlib.pyplot as plt
import os
from matplotlib import colors as mcolors

datastr = input('file:')
file1 = open(str(datastr)+'data.txt','r')


Population_size = 100
Parent_size = Population_size
Max_iteration = 1000
Selection_size = 5
Prob_crossover = 0.5
Prob_mutation = 0.1
Tabu_list_size = 5



machine = 5 #機台個數 從taillard dataset讀取
job_num = 0 #工作數量
seed = 0 # initial seed
job_seq = [] #每個工作在不同機台的加工時間
Upper_bound = 0

num_crossover = int(Population_size * Prob_crossover)
num_crossover_2 = num_crossover * 2
num_mutation = 0

def Initial_population():
    population = []
    np.random.seed(seed)
    for i in range(100):
        population.append(np.random.permutation(range(0, job_num)))
    return list(population)

def Partial_Opposed_based(p):
    bestidx = 0
    min_makespan = 1000000
    for i in range(100):
        temp = Makespan(p[i], job_num // 2)
        if (temp < min_makespan):
            min_makespan = temp
            bestidx = i
    for i in range(100):
        temp1 = list(p[i].copy())
        partial_left = list(p[bestidx].copy())
        for j in range (job_num // 2):
            temp1.remove(partial_left[j])
        p[i] = []
        p[i].extend(partial_left[:job_num//2])
        p[i].extend(temp1)
    return p

def Select_Tournament(p):
    parent = []
    for i in range(Parent_size):
        bestidx = 0
        min_makespan = 1000000
        for j in range(Selection_size):
            num = int(np.random.randint(low = 0, high = Parent_size, size = 1))
            temp = Makespan(p[num], job_num)
            if temp < min_makespan:
                min_makespan = temp
                bestidx = num
        parent.append(p[bestidx].copy())
    return parent

def Mutation(p):
    for _ in range(num_mutation):
        target = np.random.randint(num_crossover_2) # 任選一個染色體
        [j, k] = np.random.choice(job_num, 2) # 任選兩個基因
        p[target][j], p[target][k] = p[target][k], p[target][j] # 此染色體的兩基因互換
        
    return

def Crossover(p):
    offspring = []
    for i in range(num_crossover):
        mask = np.random.randint(2, size = job_num)
        [j, k] = np.random.choice(Parent_size, 2, replace = False)
        child1, child2 = p[j].copy(), p[k].copy()
        remain1, remain2 = list(p[j].copy()), list(p[k].copy())
        for j in range(job_num):
            if mask[j] == 1:
                remain2.remove(child1[j])
                remain1.remove(child2[j])
        count = 0
        for j in range(job_num):
            if mask[j] == 0:
                child1[j] = remain2[count]
                child2[j] = remain1[count]
                count += 1
        offspring.append(child1)
        offspring.append(child2)
    return offspring
    
def Crossover_Two_point(p):
    offspring = []
    for i in range(num_crossover):
        cross_point = np.random.choice(job_num, 2, replace=False)
        np.sort(cross_point)
        mask = []
        for j in range(0,cross_point[0]):
            mask.append(1)
        for j in range(cross_point[0], cross_point[1]+1):
            mask.append(0)
        for j in range(cross_point[1], job_num):
            mask.append(1)
        
        [j, k] = np.random.choice(Parent_size, 2, replace = False)
        child1, child2 = p[j].copy(), p[k].copy()
        remain1, remain2 = list(p[j].copy()), list(p[k].copy())
        for j in range(job_num):
            if mask[j] == 1:
                remain2.remove(child1[j])
                remain1.remove(child2[j])
        count = 0
        for j in range(job_num):
            if mask[j] == 0:
                child1[j] = remain2[count]
                child2[j] = remain1[count]
                count += 1
        offspring.append(child1)
        offspring.append(child2)
    return offspring

def sortChrome(job_seq_list, job_makespan):	    
    job_list_index = range(len(job_seq_list))                         
    
    job_makespan, job_list_index = zip(*sorted(zip(job_makespan,job_list_index))) 
   
    return [job_seq_list[i] for i in job_list_index], job_makespan
    
def replace(parent, parent_makespan, offspring, offspring_makespan):
    parent.extend(offspring)
    parent_makespan.extend(offspring_makespan)
    
    parent, parent_makespan = sortChrome(parent, parent_makespan)
    
    return parent[:Population_size], list(parent_makespan[:Population_size])
    
def Tabu_Search(sequence):
    best_makespan = Makespan(sequence, job_num)
    
    tabu_list = []
    current_solution = sequence.copy()
    for i in range(job_num):
        neighbor_method = list(np.random.randint(2, size=10))#Neighborhood Generation method
        neighbor_list = []#neighbors of a iteration
        neighbor_list_makespan = []# the makespan of neighbor
        for n in range(10):
            [j,k] = np.random.choice(job_num, 2, replace=False)
            current_neighbor = current_solution.copy()
            if (neighbor_method[n] == 1):#swap method 
                current_neighbor[j] ^= current_neighbor[k]
                current_neighbor[k] ^= current_neighbor[j]
                current_neighbor[j] ^= current_neighbor[k]
            else:#insert method
                pop_up_job = current_neighbor[j]
                current_neighbor.pop(j)
                current_neighbor.insert(k,pop_up_job)
            
            neighbor_list.append(current_neighbor.copy())
            neighbor_list_makespan.append(Makespan(current_neighbor, job_num))
            
        sorted_job_neighbor, sorted_makespan_neighbor = sortChrome(neighbor_list, neighbor_list_makespan)
        for n in range(10):
            if (not(sorted_job_neighbor[n] in tabu_list)):
                if (sorted_makespan_neighbor[n] < best_makespan):
                    sequence = sorted_job_neighbor[n].copy()
                tabu_list.append(current_solution.copy())
                current_solution = sorted_job_neighbor[n].copy()
                if (len(tabu_list) > Tabu_list_size):
                    tabu_list.pop(0)
                break
    return sequence

def Makespan(chrome_job, job_size):
    makespan_sumup = []
    for i in range (machine):
        temp = []
        makespan_sumup.append(temp)
    for j in range(job_size):
        for i in range(machine):
            if (i == 0 and j == 0):
                makespan_sumup[i].append(job_seq[i][chrome_job[j]])
            elif (j == 0):
                makespan_sumup[i].append(makespan_sumup[i-1][j]+job_seq[i][chrome_job[j]])
            elif (i == 0):
                makespan_sumup[i].append(makespan_sumup[i][j-1]+job_seq[i][chrome_job[j]])
            else:
                makespan_sumup[i].append(max(makespan_sumup[i-1][j], makespan_sumup[i][j-1]) + job_seq[i][chrome_job[j]])
                    
    return makespan_sumup[machine - 1][job_size - 1]



data_count = 0
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
color_list = list(colors.values())
color_list.remove((1, 1, 1))
color_list.remove('#FFFFFF')

while True:
    line = file1.readline()
    if not line:
        break
    data_count += 1
    if (data_count == 2):
        split_val = line.split()
        job_num = int(split_val[0])
        machine = int(split_val[1])
        seed = int(split_val[2])
        Upper_bound = int(split_val[3])
        population = Initial_population()#Reading parameters from file
        num_mutation = int(Prob_mutation * Population_size * job_num)
        print("Solving the next problem")
    elif (data_count >= 4):
        split_val = line.split()
        split_val = list(map(int, split_val))
        job_seq.append(split_val)
    if (data_count == machine + 3):#After reading job processing time from file
        data_count = 0
        population = Partial_Opposed_based(population)
        population_makespan = []
        np.random.seed(int(time.time()))
        for i in range(len(population)):
            population_makespan.append(Makespan(population[i], job_num))
        isEarlyStop = False
        for j in range(Max_iteration):
            Parent = Select_Tournament(population)
            Offspring = Crossover(Parent)
            Mutation(Offspring)
            Offspring_makespan = []
            for i in range(len(Offspring)):
                Offspring[i] = Tabu_Search(population[i]).copy()
                Offspring_makespan.append(Makespan(Offspring[i], job_num))
            population, population_makespan = replace(population, population_makespan, Offspring, Offspring_makespan)
            print("Iteration"+ str(j)+ ": Best Job Sequence: " +str(population[0])+ ", Makespan="+ str(population_makespan[0]))
            if (population_makespan[0] <= Upper_bound):
                print("The GA_TS hybird algorithm has reached the upper bound")
                #fp = open(str(datastr)+"Result.txt", "a")
                #fp.write("Makespan="+str(population_makespan[0])+", Iteration="+str(j)+"\n")
                #fp.close()
                isEarlyStop = True
                break
        #if (not(isEarlyStop)):
            #fp = open(str(datastr)+"Result.txt", "a")
            #fp.write("Makespan="+str(population_makespan[0])+", Iteration=999\n")
            #fp.close()

        #Decode section
        fig, Gannt_chart = plt.subplots()
        Gannt_chart.set_ylim(0, job_num * 10)
        Gannt_chart.set_xlim(0, population_makespan[0])
        Gannt_chart.set_xlabel("Makespan")
        Gannt_chart.set_ylabel("Jobs")
        yticks = []
        yticklabel = []
        for i in range(job_num):
                yticks.append(i * 10)
                yticklabel.append("Job"+str(population[0][i]))
        Gannt_chart.set_yticks(yticks)
        Gannt_chart.set_yticklabels(yticklabel)
        
        makespan_sumup = []
        for i in range (machine):
            temp = []
            makespan_sumup.append(temp.copy())
        
        for j in range (job_num):
            for i in range (machine):
                if (i == 0 and j == 0):
                    makespan_sumup[i].append(job_seq[i][population[0][j]])
                    Gannt_chart.broken_barh([(0, job_seq[i][population[0][j]])], (0, 10), facecolors=(color_list[i]))
                elif (j == 0):
                    makespan_sumup[i].append(makespan_sumup[i-1][j] + job_seq[i][population[0][j]])
                    Gannt_chart.broken_barh([(makespan_sumup[i-1][j], job_seq[i][population[0][j]])], 
                    (0, 10), facecolors=(color_list[i]))
                elif (i == 0):
                    makespan_sumup[i].append(makespan_sumup[i][j-1] + job_seq[i][population[0][j]])
                    Gannt_chart.broken_barh([(makespan_sumup[i][j-1], job_seq[i][population[0][j]])], 
                    (j*10, 10), facecolors=(color_list[i]))
                else:
                    makespan_sumup[i].append(max(makespan_sumup[i-1][j], makespan_sumup[i][j-1]) + job_seq[i][population[0][j]])
                    Gannt_chart.broken_barh([(max(makespan_sumup[i-1][j], makespan_sumup[i][j-1]), job_seq[i][population[0][j]])], 
                    (j*10, 10), facecolors=(color_list[i]))
        plt.show()
        
        print("\n")
        
        job_seq = []
file1.close()
#fp = open(str(datastr)+"Result.txt", "a")
#fp.write("\n")
#fp.close()
os.system("pause")
