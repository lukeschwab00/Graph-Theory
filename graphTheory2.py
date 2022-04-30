import pandas as pd
import numpy as np
import networkx as nx
import os
from csv import reader
import time
#data = pd.read_csv('hall_data.csv')
#another comment

class indovateNav:
    def __init__ (self, apriltag, room_number):
        self.data = pd.read_csv("hallData2.csv")
        self.rooms = pd.read_csv("NC_FF_ALPHA_NODES.csv"))
        self.df = nx.from_pandas_edgelist(self.data, source = 'tag', target = 'cluster', edge_attr='distance')
        self.room_number = room_number
        self.apriltag = apriltag
    def getAlphaNodes(self):
        index = []
        with open('NC_FF_ALPHA_NODES.csv','r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                for i in range(len(row)):
                    if self.room_number == row[i]:
                        index.append(i)     
        self.alphaNodes = []
        with open('NC_FF_ALPHA_NODES.csv','r') as read_obj:
            csv_reader = reader(read_obj)
            row1 = next(csv_reader)
            for i in index:
                self.alphaNodes.append(row1[i])
        # This is a comment to ruin your life~
        
#make a list of 10000 12s

# apriltag = input("AprilTag ID: ")
# # a = ['0' for i in range(10000)]
# # room_number = '1009A'
# room_number = input("Room Number: ")


# data = pd.read_csv(os.path.join(os.getcwd(),"hallData2.csv"))
# rooms = pd.read_csv(os.path.join(os.getcwd(),"NC_FF_ALPHA_NODES.csv"))
# df = nx.from_pandas_edgelist(data, source = 'tag', target = 'cluster', edge_attr='distance')

#Find where room is in alpha nodes
#for line in rooms:
#    print(line)

# index = []
# with open('NC_FF_ALPHA_NODES.csv','r') as read_obj:
#     csv_reader = reader(read_obj)
#     for row in csv_reader:
#         for i in range(len(row)):
#             if room_number == row[i]:
#                 index.append(i)
                
# alphaNodes = []
# with open('NC_FF_ALPHA_NODES.csv','r') as read_obj:
#     csv_reader = reader(read_obj)
#     row1 = next(csv_reader)
#     for i in index:
#         alphaNodes.append(row1[i])

# for apriltag in a:
#     start = time.time()
#     #time.sleep(0.0333)
for node in alphaNodes:
    shortest_path = nx.dijkstra_path(df, source = apriltag, target = node, weight = 'distance')
    shortest_path_length = nx.dijkstra_path_length(df, source = apriltag, target = node, weight = 'distance')
    #print(int(shortest_path_length))
destination = shortest_path[len(shortest_path)-1]
for i in shortest_path:
    if not i.isdecimal():
        shortest_path.remove(i)
shortest_path.append(destination)
print(shortest_path)

        
directions = []
firstdirection = True
for room in range(len(shortest_path)-1):
    #find the combination of two ATIDs
    path = ['','']
    path[0] = shortest_path[room]
    path[1] = shortest_path[room + 1]
    filterdata = data[(data.tag == path[0])&(data.cluster == path[1])]
    # Notice filterdata will always be empty if the two conditions are not satisfied
    if filterdata.empty:
        filterdata = data[(data.cluster == path[0])&(data.tag == path[1])]
    # Database is set up so that the first direction will work properly
    if firstdirection:
        direction = str(str(filterdata.distance.item()) + ' ' + filterdata.turn.item())
        directions.append(direction)
        firstdirection = False
        continue
    
    # This accounts for the fact that the person is most likely arriving in the opposite direction of 
    # the april tag
    if filterdata.distance.item() < 1:
        if filterdata.turn.item() == 'B':
            turn = 'F'
        elif filterdata.turn.item() == 'L':
            turn = 'R'
        elif filterdata.turn.item() == 'R':
            turn = 'L'
        elif filterdata.turn.item() == 'F':
            turn = 'B'
        direction = str(str(filterdata.distance.item()) + ' ' + turn)
        directions.append(direction)
    else:
        direction = str(str(filterdata.distance.item()) + ' ' + filterdata.turn.item())
        directions.append(direction)

#Print into simple directions
newDirection = []
for i in directions:
    i = i.split(' ')
    #print(i)
    for x in i:
        newDirection.append(x)
print(newDirection)


  
indovatePath = indovateNav(10,1402)




