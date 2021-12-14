import xml.etree.ElementTree as ET
import json
import timeit
import numpy as np
from treelib import Node, Tree


tree = Tree()


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

def split_list(alist, wanted_parts=2):  #Διαχωρισμός πίνακα στην μέση
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

def visual(PST):     #Οπτική παρουσίαση Δεντρου
    tree.create_node(PST.root.val, PST.root)
    PST.root.getChildren()


#####################################################################################

class Node: #Κλάση Κόμβων
    def init(self, val):    
        self.val = val
        self.leftChild = None
        self.rightChild = None
        self.maxormin = None

    def get(self):
        return self.val

    def set(self, val):
        self.val = val

    def getChildren(self):  #Εύρεση παιδίων κόμβου
        children = []
        if(self.leftChild != None):
            tree.create_node(self.leftChild.val, self.leftChild, parent=self)
            children.append(self.leftChild)
        if(self.rightChild != None):
            tree.create_node(self.rightChild.val, self.rightChild, parent=self)
            children.append(self.rightChild)
        
        for k in children:
            k.getChildren()

    def calcMed(self): # υπολογισμός κάθετου που χωρίζει τα σημεία σε 2 ίσα μέρη
        return (self.leftChild.maxormin + self.rightChild.maxormin)/2
        

class PST:      #Priority Search Tree
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


    def createTree(self, prev, points):     #Δημιουργία Priority Search Tree
        pointsB, pointsA = split_list(points)
        prevb = prev

        if len(pointsA) > 1:
            pointsA.sort(key=lambda x:x[1])
            prev = self.insertRightNode(prev, pointsA[-1])
            pointsA.pop(-1)
            pointsA.sort(key=lambda x:x[0])
            prev.maxormin = pointsA[0][0]
            self.createTree(prev, pointsA)
        elif len(pointsA) == 1:
            prev = self.insertRightNode(prev, pointsA[0])
            prev.maxormin = pointsA[0][0]

        if len(pointsB) > 1:
            pointsB.sort(key=lambda x:x[1])
            prevb = self.insertLeftNode(prevb, pointsB[-1])
            pointsB.pop(-1)
            pointsB.sort(key=lambda x:x[0])
            prevb.maxormin = pointsB[-1][0]
            self.createTree(prevb, pointsB)
        elif len(pointsB) == 1:
            prevb = self.insertLeftNode(prevb, pointsB[0])
            prevb.maxormin = pointsB[0][0]


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


    def Tsq(self, query, checkNode, resar):     #3 sided query
        if (checkNode.val[1]<query.val[2]):
            return
        else:
            if (checkNode.val[0]>=query.val[0] and checkNode.val[0]<=query.val[1]):
                resar.append(checkNode.val)

            if (checkNode.rightChild !=None and checkNode.leftChild != None):
                if (checkNode.calcMed()<=query.val[0]):
                    self.Tsq(query, checkNode.rightChild, resar)
                    return
                elif (checkNode.calcMed()>=query.val[1]):
                    self.Tsq(query, checkNode.leftChild, resar)
                    return
                else:
                    self.Tsq(query, checkNode.rightChild, resar)
                    self.Tsq(query, checkNode.leftChild, resar)
                    return
            elif (checkNode.rightChild !=None):
                self.Tsq(query, checkNode.rightChild, resar)
                return
            elif (checkNode.leftChild !=None):
                self.Tsq(query, checkNode.leftChild, resar)
                return
            else: return

    '''def Tsqx(self, query, checkNode, resar):     #Προσπάθεια υλοποίσης 3sided query με άπειρη τιμή στον Χ άξονα
        if checkNode.val[1]<query.val[1]:
            return
        else:
            if (checkNode.val[1]<query.val[2] and checkNode.val[0]<query.val[0]):
                resar.append(checkNode.val)

            if (checkNode.rightChild !=None and checkNode.leftChild != None):
                if (checkNode.calcMed()>query.val[0]):
                    self.Tsq(query, checkNode.rightChild, resar)
                    return
                else:
                    self.Tsq(query, checkNode.rightChild, resar)
                    self.Tsq(query, checkNode.leftChild, resar)
                    return
            elif (checkNode.rightChild !=None):
                self.Tsq(query, checkNode.rightChild, resar)
                return
            elif (checkNode.leftChild !=None):
                self.Tsq(query, checkNode.leftChild, resar)
                return
            else: return'''


class Query:    #Κλάση ορισμού ορίων query
    def init(self, minx, maxx, y):
        self.val = [minx, maxx, y]


#######################################################################################



points = []
TSQres = []

points = read_file('test.json', points)
points.sort(key=lambda x:x[1])

Prio = PST()
Prio.init()
Prio.setRoot(points[-1])
#Δημιουργία δέντρου
points.pop(-1)
prev = Prio.root
points.sort(key=lambda x:x[0])
Prio.createTree(prev, points)
#Οπτική Απεικόνιση
visual(Prio)
tree.show()
#3 sided Query
rect = Query()
rect.init(-130, 100, 150)
start = timeit.default_timer()
Prio.Tsq(rect, Prio.root, TSQres)
end = timeit.default_timer()
print("Time",end-start)
print(TSQres)
