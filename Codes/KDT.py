import xml.etree.ElementTree as ET
import json
import timeit
import numpy as np
from numpy.lib.function_base import insert, median
from treelib import Node, Tree


tree = Tree()
startDim = 1    #1=Y,0=X άξονας πρώτου διαχωρισμού του χώρου

########################################################################################

def read_file(file_name,array):     # Διαβάζει json αρχεία και αποθηκεύει τα σημεία στην λίστα array

    f = open(file_name, encoding='UTF-8')
    
    data = json.load(f)
    
    num = 0

    for i in data['data']:
        array.append(i['coordinates'])
        num = num + 1

    f.close()
    return array

def split_list(alist, wanted_parts=2):      #Διαχωρισμός πίνακα στην μέση
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

def visual(KDT):        #Οπτική παρουσίαση Δεντρου
    tree.create_node(KDT.root.val, KDT.root)
    KDT.root.getChildren()


#####################################################################################

class Node:     #Κλάση Κόμβων
    def init(self, val):
        self.val = val
        self.leftChild = None
        self.rightChild = None

    def get(self):
        return self.val

    def set(self, val):
        self.val = val

    def getChildren(self):      #Εύρεση παιδίων κόμβου
        children = []
        if(self.leftChild != None):
            tree.create_node(self.leftChild.val, self.leftChild, parent=self)
            children.append(self.leftChild)
        if(self.rightChild != None):
            tree.create_node(self.rightChild.val, self.rightChild, parent=self)
            children.append(self.rightChild)
        
        for k in children:
            k.getChildren()

class KDT: #K-D Tree
    def init(self):
        self.root = None

    def setRoot(self, val):
        node = Node()
        node.init(None)
        node.set(val)
        self.root = node

    def insertLeftNode(self, currentNode, val):
        node = Node()
        node.init(None)
        node.set(val)
        currentNode.leftChild = node

        return node

    def insertRightNode(self, currentNode, val):
        node = Node()
        node.init(None)
        node.set(val)
        currentNode.rightChild = node

        return node

    def createTree(self, prev, points, dim=startDim):       #Δημιουργία K-D Tree
        prevb = prev

        pointsB, pointsA = split_list(points)
        dim = dim + 1
        dimb=dim
        pointsA.sort(key=lambda x:x[dim%2])
        pointsB.sort(key=lambda x:x[dimb%2])
        


        if len(pointsA) > 1:
            meda = int(len(pointsA)/2 +0.5)
            prev = self.insertRightNode(prev, pointsA[meda])
            pointsA.pop(meda)
            self.createTree(prev, pointsA, dim)
        elif len(pointsA) == 1:
            self.insertRightNode(prev, pointsA[0])

        if len(pointsB) > 1:
            medb = int(len(pointsB)/2 +0.5)
            prevb = self.insertLeftNode(prevb, pointsB[medb])
            pointsB.pop(medb)
            self.createTree(prevb, pointsB, dimb)
        elif len(pointsB) == 1:
            self.insertLeftNode(prevb, pointsB[0])

        
        


    def find(self, val):
        return self.findNode(self.root, val)

    def findNode(self, currentNode, val):
        if(currentNode is None):
            return False
        elif(val == currentNode.val):
            return True
        elif(val < currentNode.val):
            return self.findNode(currentNode.leftChild, val)
        else:
            return self.findNode(currentNode.rightChild, val)

    def TSQ(self, query, checkNode, resar, mode, dim=startDim):      #3 sided query, 1 άπειρο άνω όριο,2 άπειρο κάτω όριο για την τιμή του y
        if (mode==1):
            if(checkNode.val[0]>=query.val[0] and checkNode.val[0]<=query.val[1] and checkNode.val[1]>=query.val[2]):
                resar.append(checkNode.val)
                dim = dim +1
                if (checkNode.leftChild != None):
                    self.TSQ(query, checkNode.leftChild, resar, mode, dim)
                if (checkNode.rightChild != None):
                    self.TSQ(query, checkNode.rightChild, resar, mode, dim)
                return
        elif (mode==2):   # Αλλάζει μονο η τιμή του y dim > to <
            if(checkNode.val[0]>=query.val[0] and checkNode.val[0]<=query.val[1] and checkNode.val[1]<=query.val[2]):
                resar.append(checkNode.val)
                dim = dim +1
                if (checkNode.leftChild != None):
                    self.TSQ(query, checkNode.leftChild, resar, mode, dim)
                if (checkNode.rightChild != None):
                    self.TSQ(query, checkNode.rightChild, resar, mode, dim)
                return

        if(dim%2 == 0):
            
            if(checkNode.val[0]<query.val[0]):
                dim = dim +1
                if (checkNode.rightChild != None):
                    self.TSQ(query, checkNode.rightChild, resar, mode, dim)
                return
            elif(checkNode.val[0]>query.val[1]):
                dim = dim +1
                if (checkNode.leftChild != None):
                    self.TSQ(query, checkNode.leftChild, resar, mode, dim)
                return
            else:
                dim = dim +1
                if (checkNode.leftChild != None):
                    self.TSQ(query, checkNode.leftChild, resar, mode, dim)
                if (checkNode.rightChild != None):
                    self.TSQ(query, checkNode.rightChild, resar, mode, dim)
                return
        elif(dim%2 == 1):
            if(checkNode.val[1]<query.val[2] and mode==1):
                dim = dim +1
                if (checkNode.rightChild != None):
                    self.TSQ(query, checkNode.rightChild, resar, mode, dim)
                return
            elif(checkNode.val[1]>query.val[2] and mode==2):
                dim = dim +1
                if (checkNode.leftChild != None):
                    self.TSQ(query, checkNode.leftChild, resar, mode, dim)
                return
            else:
                dim = dim +1
                if (checkNode.leftChild != None):
                    self.TSQ(query, checkNode.leftChild, resar, mode, dim)
                if (checkNode.rightChild != None):
                    self.TSQ(query, checkNode.rightChild, resar, mode, dim)
                return

class Query:        #Κλάση ορισμού ορίων query
    def init(self, minx, maxx, y):
        self.val = [minx, maxx, y]


#######################################################################################



points = []
TSQres = []

points = read_file('test.json', points)
points.sort(key=lambda x:x[startDim])
#Δημιουργία δέντρου
Prio = KDT()
Prio.init()
med = int(len(points)/2)
Prio.setRoot(points[med])
points.pop(med)
Prio.createTree(Prio.root, points, startDim)
#Οπτική Απεικόνιση
visual(Prio)
tree.show()
#3 sided Query
rect = Query()
rect.init(-130, 150, 0)
start = timeit.default_timer()
Prio.TSQ(rect, Prio.root, TSQres, 1)
end = timeit.default_timer()
print("Time",end-start)
print(TSQres)