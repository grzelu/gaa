import numpy as np
from generic_algorythm.geny import City

population_size = 60
route_size = 8
crossover_probability = 0.8
mutation_probability = 0.008
data_path = "vars/DANE.txt"
data_matrix = np.loadtxt(data_path,skiprows=25)
flow_matrix = data_matrix
#print (flow_matrix)

data_file = open(data_path,'r')
city_list = []
flow_list = []
flow=False
counter = 0

while True:

    line = data_file.readline().strip('\r\n')
    #print(line)
    if line=='---':
        data_file.close()
        break
    temp = line.split(' ')

    #city_list.append(.append(counter))
    city_list.append({'idx':counter, 'name':temp[0],'x':temp[1],'y':temp[2]})
    counter += 1



chromosome_list = [City(i, flow_matrix) for i in city_list]
print (chromosome_list)