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
        self.rooms = pd.read_csv("NC_FF_ALPHA_NODES.csv")
        self.df = nx.from_pandas_edgelist(self.data, source = 'tag', target = 'cluster', edge_attr='distance')
        self.room_number = str(room_number)
        self.apriltag = str(apriltag)
        self.getAlphaNodes()
        self.shortestPath()
        self.simplifyShortestPath()
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

    def shortestPath(self):
        for node in self.alphaNodes:
            self.shortest_path = nx.dijkstra_path(self.df, source = self.apriltag, target = node, weight = 'distance')
            #shortest_path_length = nx.dijkstra_path_length(df, source = apriltag, target = node, weight = 'distance')
            #print(int(shortest_path_length))
        destination = self.shortest_path[len(self.shortest_path)-1]
        for i in self.shortest_path:
            if not i.isdecimal():
                self.shortest_path.remove(i)
        self.shortest_path.append(destination)
        # This is a comment to ruin your life~
    def simplifyShortestPath(self):
        directions = []
        firstdirection = True
        for room in range(len(self.shortest_path)-1):
            #find the combination of two ATIDs
            path = ['','']
            path[0] = self.shortest_path[room]
            path[1] = self.shortest_path[room + 1]
            filterdata = self.data[(self.data.tag == path[0])&(self.data.cluster == path[1])]
            # Notice filterdata will always be empty if the two conditions are not satisfied
            if filterdata.empty:
                filterdata = self.data[(self.data.cluster == path[0])&(self.data.tag == path[1])]
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
        self.newDirection = newDirection
        
        parSum = 0
        
        simpleDirection = []
        for i in range(len(newDirection)):
            if i % 2 == 1:
                if i == len(newDirection)-1:
                    if newDirection[i] == 'F':   
                        simpleDirection.append(int(float(newDirection[i-1])))
                        simpleDirection.append(newDirection[i])
                        pass
                # if i == len(newDirection):
                #     simpleDirection.append(newDirection[i])
                if newDirection[i] == 'F':
                    parSum = parSum + float(newDirection[i-1])
                else:
                    if parSum == 0:
                        simpleDirection.append(int(float(newDirection[i-1])))
                        simpleDirection.append(newDirection[i])
                        pass
                    else:
                        simpleDirection.append(int(float((parSum))))
                        simpleDirection.append('F')
                        simpleDirection.append(int(float(newDirection[i-1])))
                        simpleDirection.append(newDirection[i])
                        parSum = 0
                    # if not fwdFlag:
                    #     simpleDirection.append(newDirection[i-1])
                    #     simpleDirection.append(newDirection[i])
                    #     parSum = 0
                    # if fwdFlag:
                    #     simpleDirection.append(parSum)
                    #     simpleDirection.append('F')
                    #     fwdFlag = False
        self.newDirection = simpleDirection

  
indovatePath = indovateNav("12","1005")
print(indovatePath.newDirection)
# print(indovatePath.shortest_path)
# print(indovatePath.simpleDirection)



