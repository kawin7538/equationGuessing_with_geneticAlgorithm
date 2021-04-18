import numpy as np 
import math
import copy
from numpy.random import randint

# Solve 2A + 4B + 3C + 2D 

MIN_NUM=1
MAX_NUM=1000
CNT_POPULATION=40

def get_equation_sum(a,b,c,d):
    return math.pow(a,4)-math.pow(b,3)-math.pow(c,2)+d
    # return math.pow(a-b,4)-math.pow(c-d,4)
    # return math.pow(a,3)-math.pow(b,2)+math.pow(c,2)-d
    # return a*b*c*d

def objective_func(a,b,c,d,expect_ans=0):
    return np.abs(get_equation_sum(a,b,c,d)-expect_ans)

def fitness_func(obj_value):
    return 1/(1+obj_value)

def get_r():
    r=np.random.rand(CNT_POPULATION)
    return r

def get_crossover_prob():
    crossover_prob=get_r()
    return crossover_prob/np.sum(crossover_prob)

def get_init_chromosome():
    return np.array([[randint(MIN_NUM,MAX_NUM),randint(MIN_NUM,MAX_NUM),randint(MIN_NUM,MAX_NUM),randint(MIN_NUM,MAX_NUM)] for i in range(CNT_POPULATION)])

if __name__ == '__main__':
    f=open('output.txt','w')
    chromosome = get_init_chromosome()
    iter_round=0
    while True:
        iter_round+=1
        f_obj=np.array([objective_func(a,b,c,d) for a,b,c,d in chromosome])
        if np.min(f_obj)!=0:
            f.write("Round : {} Min : {} - Population : {}\n".format(iter_round, min(f_obj), chromosome))
            print("Round : {} Min : {}".format(iter_round, min(f_obj)))
        else:
            f.write('-'*40)
            f.write("\n")
            f.write("Round : {} Min : {} - Population : {}\n".format(iter_round, min(f_obj), chromosome))
            f.write("Best Chromosome : {}\n".format(chromosome[np.where(f_obj==0)]))
            f.write("End")
            print('-'*40)
            print("\n")
            print("Round : {} Min : {}".format(iter_round, min(f_obj)))
            print("Best Chromosome : {}".format(chromosome[np.where(f_obj==0)]))
            print("End")
            break;
        # print("objective function",f_obj)
        fitness=fitness_func(f_obj)
        # print("fitness function",fitness)
        p=fitness/np.sum(fitness)
        # print("p",p)
        c=np.cumsum(p)
        # print("c",c)
        r=get_r()
        # print("r",r)

        #selecting new gene
        new_idx_chromosome=np.zeros(CNT_POPULATION)
        for r_idx in range(CNT_POPULATION):
            for c_idx in range(CNT_POPULATION):
                if r[r_idx]<=c[c_idx]:
                    new_idx_chromosome[r_idx]=c_idx
                    break;
        # print("new index",new_idx_chromosome)
        new_chromosome=np.array(chromosome)[new_idx_chromosome.astype('int')]
        # print("new chromosome",new_chromosome)
        crossover_rate=0.30
        crossover_prob=get_crossover_prob()
        # print("crossover Prob",crossover_prob)
        parent_idx=np.where(crossover_prob<=crossover_rate)[0]
        parent=new_chromosome[parent_idx]
        # print("parent",parent)
        # backup_new_chromosome=copy.deepcopy(new_chromosome)

        #crossover
        if len(parent)>1:
            for i in range(len(parent)):
                cut_idx=randint(1,3)
                if i==len(parent)-1:
                    new_chromosome[parent_idx[i]]=np.concatenate((parent[i][:cut_idx],parent[0][cut_idx:]))
                else:
                    new_chromosome[parent_idx[i]]=np.concatenate((parent[i][:cut_idx],parent[i+1][cut_idx:]))
        # print("after crossover",new_chromosome)

        #mutation
        mutation_rate=0.2
        cnt_mutate=np.floor(CNT_POPULATION*4*mutation_rate)
        idx_mutate=randint(0,4*CNT_POPULATION,cnt_mutate.astype('int'))
        # print(idx_mutate)
        temp_new_chromosome=copy.deepcopy(new_chromosome)
        temp_new_chromosome=np.ravel(temp_new_chromosome)
        for idx in idx_mutate:
            temp_new_chromosome[idx]=randint(MIN_NUM,MAX_NUM)
        new_chromosome=temp_new_chromosome.reshape((-1,4))
        # print(new_chromosome)
        chromosome=new_chromosome