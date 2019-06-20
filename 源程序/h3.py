# -*- coding: utf-8 -*-
import numpy as np
from random import randrange

#将牌在位时的正确坐标
correctPos = {1:[0, 0], 2:[0, 1], 3:[0,2], 
                   4:[1, 2], 5:[2, 2], 6:[2,1],  
                   7:[2, 0], 8:[1, 0]}

class State:
    def __init__(self, state, directionFlag=None, parent=None):
        self.state = state             
        self.direction = ['up', 'down', 'right', 'left']
        if directionFlag:
            self.direction.remove(directionFlag)            
        self.parent = parent
        self.symbol = ' '
        self.fn = 0    #耗散值
#        self.dn = 0    #当前结点的深度
        self.hn = 0    #当前结点不在位的将牌数
        self.isInOpen = False
        self.isNew = True

    def GetEmptyPos(self):
        postion = np.where(self.state == self.symbol)
        return postion
    
    def GetSn(self):  #求sn
        tempState = self.state.copy()
        weight = 0
        if(tempState[1,1] == ' '):
            weight = 1
        else:
            weight = 0
        for y in  range(1,3):   #第一行
            if(tempState[0][y] != y + 1):
                weight += 2
                
        for x in range(1,3):   #第三列
            if(tempState[x][2] != 3 + x):
                weight += 2
                
        if(tempState[2][1] != 6):
            weight += 2
        if(tempState[2][0] != 7):
            weight += 2
        if(tempState[0][0] != 1):
            weight += 2
        
        return weight
        
    def GetHn(self):
        self.hn = self.GetPn() + 3*self.GetSn()
    
    def GetPn(self): #更新当前结点不在位将牌
        distance = 0
        temp = 0
        tempState = self.state.copy()
        for x in range(0,3):
            for y in range(0,3):
                if(' ' == tempState[x,y]):
                    continue
                temp = int(tempState[x,y])
                distance += abs(correctPos[temp][1] - y)
                distance += abs(correctPos[temp][0] - x) 
                
        return distance
        
    def GetDeepth(self):   #计算当前结点的深度，根节点深度为0
        deepth = 0
        path = []    #临时存储指针，用于恢复结点的parent
        path.append(self)
        while self.parent and self.parent != originState:  
            path.append(self.parent)
            self = self.parent
            deepth += 1
            
        #恢复parent的指向
        length = len(path)
        i = 0
        while(i < length - 1):
            path[i].parent = path[i + 1]
            i += 1
        return deepth
    
    def GetDirection(self):
        return self.direction
    
    def GetPath(self):   #返回含有目标的搜索路径
        path = []
        path.append(self)
        while self.parent and self.parent != originState:  #记录含有目标的路径
            path.append(self.parent)
            self = self.parent
        path.reverse()
        return path
        
    def SeekTarget(self):    
        OPEN = []                  
        CLOSED = []                 
        OPEN.append(self)    
        steps = 1  
        nodeNumber = 0
        while len(OPEN) > 0:      
            n = OPEN.pop(0)
            n.isInOpen = False
            
            CLOSED.append(n)
            childStates = n.Expand()  #（6）开始扩展当前结点
            nodeNumber += len(childStates)
            """
            拓展出来的结点有三种可能：
            1.之前没有生成过的新结点
            2.当前在OPEN中的结点
            3.已经被Expand的结点
            """
            for s in childStates:
                if (s.state == s.answer).all():
                    #如果s为目标结点，则返回路径及step
                    s.parent = n
                    return s.GetPath(),steps+1,nodeNumber
                
                if (True == s.isNew):    #当前结点为首次出现
                    s.GetHn()
                    s.parent = n
                    s.fn = s.GetDeepth() + s.hn
                    s.isInOpen = True
                    s.isNew = False
                    OPEN.append(s)

                elif (True == s.isInOpen):  #当s当前已在OPEN中
                    indexOfS = OPEN.index(s)
                    s = OPEN.pop(indexOfS)   #将s从OPEN中取出
                    newDeepth = n.GetDeepth() + 1
                    if(s.GetDeepth() > newDeepth):
                        #f(n,mk)和f(mk)之间的比较其实就是深度的比较
                        s.fn = s.wn + newDeepth
                        s.parent = n
             #       print("第二种情况")
                    
                else:  #第三种情况：当前结点已经被扩展过
                    newDeepth = n.GetDeepth() + 1
                    if(s.GetDeepth() > newDeepth):
                        s.parent = n
                        s.fn = s.wn + newDeepth
                        OPEN.append(s)
         #           print("第三种情况")
            steps += 1
            OPEN.sort(key = GetFn)
            #（7）OPEN中的结点按f值由小到大排序
        else:
            return None

    def Expand(self):  #扩展当前结点
        if not self.direction:
            return []
        childStates = []
        boarder = len(self.state) - 1         
        
        row, col = self.GetEmptyPos()
        if 'up' in self.direction and row > 0:   #判断是否可以向上移动 
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row-1, col]
            s[row-1, col] = temp[row, col]
            news = State(s, directionFlag='down')
            childStates.append(news)
             
        if 'down' in self.direction and row < boarder: #是否可以向下移动
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row+1, col]
            s[row+1, col] = temp[row, col]
            news = State(s, directionFlag='up')
            childStates.append(news)
        
        if 'left' in self.direction and col > 0:#是否可以向左移动
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col-1]
            s[row, col-1] = temp[row, col]
            news = State(s, directionFlag='right')
            childStates.append(news)
        
        if self.direction.count('right') and col < boarder:    #是否可以向右移动
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col+1]
            s[row, col+1] = temp[row, col]
            news = State(s, directionFlag='left')
            childStates.append(news)
        return childStates
    
def GetFn(s):   #返回当前结点的耗散值
        return s.fn
    
def GenerateMatrixAuto():  #自动生成矩阵
#    NewState = np.array([[2, ' ' , 5], [8, 1 , 4], [7, 6, 3]]).copy()
#    NewState = np.array([[2, 1 , 5], [8, ' ' , 4], [7, 6, 3]]).copy()
    NewState = np.array([[2, ' ' , 3], [1, 8 , 4], [7, 6, 5]]).copy()
#    return NewState
    emptyPosX = 0;
    emptyPosY = 1;
    X = Y = 0;
    while(1):
        X = randrange(0,3)
        Y = randrange(0,3)
        if(NewState[X][Y] != NewState[emptyPosX][emptyPosY]):
            temp = NewState[X,Y]
            NewState[X,Y] = NewState[emptyPosX,emptyPosY]
            NewState[emptyPosX,emptyPosY] = temp
            break
    print(NewState)
    return NewState
     
def GenerateMatrixHand(): #手动输入矩阵
    NewState = np.array([[2, ' ' , 3], [1, 8 , 4], [7, 6, 5]]).copy()
    str = input("请依次输入矩阵元素，0代表空格: ")
    inputMatrix = []
    inputMatrix = str.split(",")
    emptyPos = inputMatrix.index('0')
    count = 0
    while(count < 9):
        if(count != emptyPos):
            NewState[count // 3,count % 3] = int(inputMatrix[count])
        else:
            NewState[count // 3,count % 3] = ' '
        count = count + 1
    print(NewState)
    return NewState

if __name__ == '__main__':
    while(1):
        choic =eval(input("输入1选择自动生成初始状态|输入2手动输入初始状态|输入3选择默认初始状态: "))
        if choic != 1 and choic != 2 and choic != 3:
            print("输入有误！","\n")
        else:
            break
    print("生成的初始状态为: ")
    if(choic == 1):
        originState = State(GenerateMatrixAuto())
    elif(choic == 2):
        originState = State(GenerateMatrixHand())
    else:
 #       newState = np.array([[2, ' ' , 3], [1, 8 , 4], [7, 6, 5]]).copy()
        newState = np.array([[2, ' ' , 5], [1, 3 , 4], [7, 6, 8]]).copy()
        originState = State(newState)
        print(newState)
        
    State.answer = np.array([[1, 2, 3], [8, ' ', 4], [7, 6, 5]])        
    s = State(state=originState.state)
    path, steps,nodeNumber = s.SeekTarget()
    if path:   #打印含目标结点的路径
        print("从起始状态到目标结点的路径为: ")
        for node in path:    
                print(node.state)
                print("      |")
                print("      v")
        print("扩展结点数为：%d" %steps)
        print("生成结点数为：%d" %nodeNumber)
    else:
        print("目标结点不可到达")