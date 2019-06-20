# -*- coding: utf-8 -*-
import numpy as np
from random import randrange
class State:
    def __init__(self, state, directionFlag=None, parent=None):
        self.state = state             
        self.direction = ['up', 'down', 'right', 'left']
        if directionFlag:
            self.direction.remove(directionFlag)            
        self.parent = parent
        self.symbol = ' '

    def GetEmptyPos(self):
        postion = np.where(self.state == self.symbol)
        return postion
    
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
            CLOSED.append(n)
            childStates = n.Expand()    #
            nodeNumber += len(childStates)
            for s in childStates:
                if (s.state == s.answer).all():  #判断是否所有的元素都是匹配的
                    return s.GetPath(),steps+1,nodeNumber
            OPEN.extend(childStates)   #添加到OPEN
            steps += 1
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
            news = State(s, directionFlag='down', parent=self)
            childStates.append(news)
             
        if 'down' in self.direction and row < boarder: #是否可以向下移动
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row+1, col]
            s[row+1, col] = temp[row, col]
            news = State(s, directionFlag='up', parent=self)
            childStates.append(news)
        
        if 'left' in self.direction and col > 0:#是否可以向左移动
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col-1]
            s[row, col-1] = temp[row, col]
            news = State(s, directionFlag='right', parent=self)
            childStates.append(news)
        
        if self.direction.count('right') and col < boarder:    #是否可以向右移动
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col+1]
            s[row, col+1] = temp[row, col]
            news = State(s, directionFlag='left', parent=self)
            childStates.append(news)
        return childStates

    

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
#        newState = np.array([[2, ' ' , 3], [1, 8 , 4], [7, 6, 5]]).copy()
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
        print("生成结点数为: %d" %nodeNumber)
    else:
        print("目标结点不可到达")