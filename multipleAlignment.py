from array import *
import numpy as np


def printTree():
    
    print("\nTree:")
    global treeStr
    global treeCounter
    
    for i in range(len(treeStr)):
        for j in range(len(treeStr[0])):
            
            if(treeStr[i][j] != 0):
                print(treeStr[i][j],end='')
        treeCounter -= 1
        if(treeCounter == 0):
            break
        else:
            print()
           
                
                
        
            
#########################################################################################################################################################################################

def toString(s):                        #Converts list's reverse to string.   
    
    str1 = "" 
    temp = []    
    temp.append(s[::-1])
   
    for i in temp[0]:
        str1 += i
            
    return str1


#########################################################################################################################################################################################
# Function to convert  
def listToString(s):  #https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1
#########################################################################################################################################################################################

def printArray(array):  
    
    print("\nSimilarity matrix:\n")
    for i in name:
        print("   ", i[0:2], end = '')
    print()
    counter = 0
    for i in array:
        print(name[counter][0:2]," ", end = '')
        counter += 1
        for j in i:
            print("{:.2f}".format(j)," ", end = '')
        print()
        
                
 
#########################################################################################################################################################################################
       
def matchMismatchScore(first,second):    #Returns blosum value. The values of Match-mismatch is taken from Blosum62 matrix. 
    index1 = blosumNames[0].index(first)
    index2 = blosumNames[0].index(second)
    return blosumMatrix[index1][index2]

#########################################################################################################################################################################################

def pairwiseAlignment(first,second,index1,index2): 

    #In this function,pairwise alignment operation is done. 
    #directions: L (left), D (diagonal), U (up), N (null)  
    
    for i in range(len(scoreMatrix)):           #row
        for j in range(len(scoreMatrix[0])):    #column
            if(i == 0 and j == 0):
                scoreMatrix[0][0] = 0
                directions[0][0] = 'N'
            elif(i == 0 and j != 0):
                scoreMatrix[i][j] = scoreMatrix[i][j-1] + penalty
                directions[i][j] = 'L'
            elif(i != 0 and j == 0):
                 scoreMatrix[i][j] = scoreMatrix[i-1][j] + penalty
                 directions[i][j] = 'U'
            else:
                diagonalScore = int(matchMismatchScore(second[i-1],first[j-1]))
                
                diagonal = scoreMatrix[i-1][j-1] + diagonalScore
                left = scoreMatrix[i][j-1] + penalty
                up = scoreMatrix[i-1][j] + penalty
                
              
                
                maxVal = max(diagonal,left,up)
                scoreMatrix[i][j] = maxVal
                
                if(left == up and up == diagonal):
                    directions[i][j] = 'LUD'
                elif(left == up and left > maxVal):
                    directions[i][j] = 'LU'
                elif(left == diagonal and left > maxVal):
                    directions[i][j] = 'LD'
                elif(diagonal == up and diagonal > maxVal):
                    directions[i][j] = 'UD'
                elif(maxVal == left):
                    directions[i][j] = 'L'
                elif(maxVal == up):
                    directions[i][j] = 'U'
                elif(maxVal == diagonal):
                    directions[i][j] = 'D'
                
    printMatrix(index1,index2)
#########################################################################################################################################################################################

def printMatrix(index1,index2): #Backtracking.
    similarityCounter = 0
    similarityScore = 0
    directionRowLen = len(directions)
    directionColumnLen = len(directions[0])
    scoreMatrixRowLen = len(scoreMatrix)
    scoreMatrixColumnLen = len(scoreMatrix[0])
    directionLastElement = directions[directionRowLen-1][directionColumnLen-1]
    row = directionRowLen - 1
    column = directionColumnLen - 1
    
    firstStr = []
    secondStr = []
    
    global rowIndex
    
    
    while(directionLastElement != directions[0][0]):
        
       
           
        if(directionLastElement == 'L' or directionLastElement == 'LUD' or directionLastElement == 'LU' or directionLastElement == 'LD'):
            firstStr.append(firstSeq[column - 1])
            secondStr.append("-")
            column -= 1
            directionLastElement = directions[row][column]
            
        elif(directionLastElement == 'U' or directionLastElement == 'UD'):
            firstStr.append("-")
            secondStr.append(secondSeq[row - 1])
            row -= 1
            directionLastElement = directions[row][column]
            
        elif(directionLastElement == 'D'):
            
            if(secondSeq[row - 1] == firstSeq[column - 1]):     #Match sequence
                firstStr.append(firstSeq[column - 1])
                secondStr.append(firstSeq[column - 1])
                similarityCounter += 1
                
            else:           #Mismatch sequence
                firstStr.append(firstSeq[column - 1])
                secondStr.append(secondSeq[row - 1])
            row -= 1
            column -= 1
            directionLastElement = directions[row][column]
            
    similarityScore = similarityCounter / len(firstStr)
    similarityMatrix[index1][index2] = similarityScore
    similarityMatrix[index2][index1] = similarityScore
    
    print(name[index1],''.join(firstStr[::-1]))        
    print(name[index2],''.join(secondStr[::-1]))
    
    sequences[rowIndex][0] = name[index1]                       #Filling sequences list with pairwise alignments.
    sequences[rowIndex][1] = toString(firstStr)
    sequences[rowIndex][2] = name[index2] 
    sequences[rowIndex][3] = toString(secondStr)
    
    rowIndex += 1
    print()
    
    
#########################################################################################################################################################################################

def neighbourJoining():
    global QCounter
    calculateU()
    calculateQ()
    QCounter += 1
    calculateD()
    
    
#########################################################################################################################################################################################
def calculateQ():
    
    #Q(i,j) = (r-2)*d(Ci,Cj) - u*Ci - uCj
    
    
    for i in range(len(similarityMatrix)):
        for j in range(len(similarityMatrix[0])):
            if(i == j):
                Q[i][j] = 0
                if(firstR == r):
                    QTemp[i][j] = "{:.2f}".format(Q[i][j])
            else:
                Q[i][j] = (r-2) * similarityMatrix[i][j] - u[i] - u[j]
                if(firstR == r):
                    QTemp[i][j] = "{:.2f}".format(Q[i][j])
    
    
    
    print("\nQ Matrix\n")
    
    for i in range(r):
        print("\t",nameUpdate[i],"\t", end = '')
            
    print()    
        
    for i in range(r):
        print(nameUpdate[i]," ",end='')
        for j in range(r):
            print("\t{:.2f}".format(Q[i][j]),"    ", end = '')
        print()
            
#########################################################################################################################################################################################

def calculateU():
    
    print("\nU Matrix\n")
    sum = 0
    count = 0
    counter = 0
    sumArray = []
    
    for i in similarityMatrix:
        for j in i:
            sum += j
        u[count] = sum
        count += 1
       
        sumArray.append(sum)
        sum = 0
        
    
    for i in range(r):
        print(nameUpdate[i],end = '')
        print("\t{:.2f}".format(sumArray[i]),"", end = '')
        print()
    sumArray.clear()
#########################################################################################################################################################################################
def calculateLength(firstChar,secondChar): 
    global clcounter
    if(clcounter==0):
        if(r>2):
            newLength1 = (similarityMatrix[firstChar][secondChar] / 2) + ((u[firstChar] - u[secondChar]) / (2 * (r - 2)))
            newLength2 = (similarityMatrix[firstChar][secondChar] / 2) + ((u[secondChar] - u[firstChar]) / (2 * (r - 2)))
        elif(r==2):
            newLength1 = similarityMatrix[firstChar][secondChar] / 2
            newLength2=newLength1
        length[clcounter][0]= name[firstChar][0:2]
        length[clcounter][1] = float(newLength1)
        print("Length of ", name[firstChar][0:2], "is {:.2f}".format(float(newLength1)) )
        clcounter +=1        
        length[clcounter][0]= name[secondChar][0:2]
        length[clcounter][1] = float(newLength2)
        print("Length of ", name[secondChar][0:2], "is {:.2f}".format(float(newLength2)) )
        clcounter +=1
    else:
        if(r>2):
            newLength1 = (similarityMatrix[firstChar][secondChar] / 2) + ((u[firstChar] - u[secondChar]) / (2 * (r - 2)))
            newLength2 = (similarityMatrix[firstChar][secondChar] / 2) + ((u[secondChar] - u[firstChar]) / (2 * (r - 2)))
        elif(r==2):
            newLength1 = similarityMatrix[firstChar][secondChar] / 2
            newLength2=newLength1
        length[clcounter][0]= nameUpdate[firstChar]
        length[clcounter][1] = float(newLength1)
        print("Length of ", nameUpdate[firstChar], "is {:.2f}".format(float(newLength1)) )
        clcounter +=1
        length[clcounter][0]= nameUpdate[secondChar]
        length[clcounter][1] = float(newLength2)
        print("Length of ", nameUpdate[secondChar], "is {:.2f}".format(float(newLength2)) )
        clcounter +=1

#########################################################################################################################################################################################
def updateD(firstChar,secondChar):
    
    #d(Ck,Cm) = (d(Ci,Cm) + d(Cj,Cm) - d(Ci,Cj)) / 2
    global r
    r -= 1
    
    
    for i in range(len(similarityMatrix)):
        for j in range(len(similarityMatrix[0])):
            
            if((i == firstChar and j == secondChar) or (i == secondChar and j == firstChar)):
                D[min(i,j)][min(i,j)] = 0
                
            elif(i == min(firstChar,secondChar)):    
                D[min(firstChar,secondChar)][j] = (similarityMatrix[firstChar][j] + similarityMatrix[secondChar][j] - similarityMatrix[firstChar][secondChar]) /2
                
            elif(j == min(firstChar,secondChar)):                
                D[i][min(firstChar,secondChar)] = (similarityMatrix[i][firstChar] + similarityMatrix[i][secondChar] - similarityMatrix[firstChar][secondChar]) /2
                
            elif(i < max(firstChar,secondChar)):                
                if(j < max(firstChar,secondChar)):                   
                    D[i][j] = similarityMatrix[i][j]                    
                elif(j > max(firstChar,secondChar)):                    
                    D[i][j-1] = similarityMatrix[i][j]                    
           
            elif(i > max(firstChar,secondChar)):               
                if(j > max(firstChar,secondChar)):                    
                    D[i-1][j-1] = similarityMatrix[i][j]                    
                elif(j < max(firstChar,secondChar)):                   
                    D[i-1][j] = similarityMatrix[i][j]
                    
                
    for i in range(len(D)):
        for j in range(len(D[0])):
            similarityMatrix[i][j] = D[i][j]
            

    
    print("\nD Matrix\n")
    
    for i in range(r):
        if(i != firstChar and i != secondChar):
            print("    ",nameUpdate[i], end = '')
        else:
            print("       ",nameUpdate[i],end='')
    print()    
    
    for i in range(r):
        if(i != firstChar and i != secondChar):
            print(nameUpdate[i],"    ", end = '')
        else:
            print(nameUpdate[i]," ",end='')
            
        for j in range(r):
            
            print("{:.2f}".format(D[i][j]),"    ", end = '')
        print()

#########################################################################################################################################################################################
def calculateD():
    global treeStr
    global treeIndex
    global treeCounter
    global maCounter
    global names1
    global names2
    minQ = 1000000
    firstChar = -1
    secondChar = -1
    
    for i in range(len(Q)):
        for j in range(len(Q[0])):
            if(Q[i][j] < minQ):
                minQ = Q[i][j]
                firstChar = i
                secondChar = j
                
   
    print("\nMinQ is: ", "{:.2f}".format(minQ))
    print("MinQ pairs: ",nameUpdate[firstChar],"and",nameUpdate[secondChar], "are joining")
    calculateLength(firstChar,secondChar)   
    treeStr[treeIndex][0] = "["  
    treeStr[treeIndex][1] = temp[firstChar]
    treeStr[treeIndex][2] = ","   
    treeStr[treeIndex][3] = temp[secondChar]   
    treeStr[treeIndex][4] = "]"
    treeIndex += 1
    treeCounter += 1
    mq = 0
    if(firstR == r):
        for i in range(len(sequences)):
            if(sequences[i][0] == name[firstChar] and sequences[i][2] == name[secondChar]):
                multipleAlignment[0][0] = name[firstChar]
                multipleAlignment[0][1] = sequences[i][1]
                multipleAlignment[1][0] = name[secondChar] 
                multipleAlignment[1][1] = sequences[i][3]
                maCounter = 1
                
    else:
        for x in name:
            if(x[0:2] == nameUpdate[secondChar]):
                sc = x[0:2]
       
        arr = nameUpdate[firstChar].split(",")
        
      
        for i in range(len(sequences)):
            if(sequences[i][0]!=0):
                if(sequences[i][0][0:2] == sc):
                    for j in arr:   
                        if(j == sequences[i][2][0:2]):
                            for k in range(len(name)):        
                                if(name[k][0:2] == j):
                                    for g in range(len(name)):
                                        if(name[g][0:2] == sc):
                                            mq = QTemp[k][g]      
                                            multipleAlignment[maCounter][0] = name[g]
                                            multipleAlignment[maCounter][1] = sequences[i][1]
                elif(sequences[i][2][0:2] == sc):
                    for j in arr:
                        if(j == sequences[i][0][0:2]):
                            for k in range(len(name)):     
                                if(name[k][0:2] == j):
                                    for g in range(len(name)):
                                        if(name[g][0:2] == sc):
                                            if(QTemp[k][g]<mq):
                                                multipleAlignment[maCounter][0] = name[g]
                                                multipleAlignment[maCounter][1] = sequences[i][3]
    maCounter += 1

                
                
    for i in range(len(nameUpdate)):
        if(i == firstChar):
            nameUpdate[i] =  nameUpdate[i] + "," + nameUpdate[secondChar] 
            temp[i] = "(" + temp[i] + "," + temp[secondChar] + ")"
            break
            
    nameUpdate.remove(nameUpdate[secondChar])
    temp.remove(temp[secondChar])
            
    
            
    updateD(firstChar,secondChar)
    
    
    
    
####################################################################    MAIN    ##########################################################################################################################################################################################################################################  

#Reading file.
fileName = "input2.txt"
blosumFile = "Blosum62.txt"
    
#Input file variables
sequence = []
name = []
dict = {}
    
#Blosum file variables.
count = 0
penalty = int(input("Gap penalty: \n"))
blosumMatrix = []
blosumNames = []
score = []
directions = []
QCounter=0
clcounter=0
temp = []

treeStr = [[0 for i in range(10)]for j in range(10)]
treeIndex = 0
treeCounter = 0

with open(fileName) as file:
    for line in file:
        if(line.strip()!=""):        
            if(line[0] == ">"):
                name.append(line[1:].strip())            
            else:
                sequence.append(line.strip())
    
r = len(name) 
firstR = r
nameUpdate = []
for i in range(len(name)):
    nameUpdate.append(name[i][0:2])
    temp.append(name[i][0:2])


with open(blosumFile) as file:
    for line in file: 
        if(count == 0):
            blosumNames.append(line.strip().split())
            count += 1
        else:
            blosumMatrix.append(line[1:].strip().split())
            count += 1


#Similarity variables   
similarityMatrix = [[0 for i in range(len(sequence))]for j in range(len(sequence))]
similarityCounter = 0
similarityScore = 0

rowIndex = 0
colIndex = 0
number = len(name[i]) * (len(name[i]) - 1)
sequences = [[0 for i in range(4)]for j in range(number)]  
names1=""
names2=""

for i in range(len(sequence)): 
    for j in range(i+1,len(sequence)):
        firstSeq = sequence[i]
        secondSeq = sequence[j]
        scoreMatrix = [[0 for i in range(len(firstSeq)+1)]for j in range(len(secondSeq)+1)]   #İlk okunan --> w (sütunlar), diğeri: v (satırlar)
        directions = [[0 for i in range(len(firstSeq)+1)]for j in range(len(secondSeq)+1)]   #İlk okunan --> w (sütunlar), diğeri: v (satırlar)
        pairwiseAlignment(firstSeq,secondSeq,i,j)

printArray(similarityMatrix)


#Neighbour Joining variables
u = np.zeros([len(name),1])
Q = np.zeros([len(name),len(name)])
D = np.zeros([len(name),len(name)])
l=len(name)*(len(name)-1)
l=int(l/2)
length = [[0 for i in range(2)]for j in range(l)]

QTemp = np.zeros([len(name),len(name)])

#Multiple sequence variables
maCounter = 0
multipleAlignment = [[0 for i in range(2)]for j in range(len(name))]

while(len(nameUpdate) > 1):
    neighbourJoining()

printTree()

print("\nMultiple Alignment\n")
for i in range(len(multipleAlignment)):
    print(multipleAlignment[i][0],"   ",listToString(multipleAlignment[i][1]))



































# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

