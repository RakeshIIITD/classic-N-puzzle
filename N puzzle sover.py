
# coding: utf-8

################################################
# AI Assignment 1
# Rakesh Rawat MT17046
################################################

from Queue import Queue,PriorityQueue
import sys
import copy
sys.setrecursionlimit(20000)


# In[2]:

################################################
# initial examples top start with 
################################################
start =            ((1,8,2),
                    (0,4,3),
                    (7,6,5))
start2 = ((1,2,3),
        (4,5,0),
         (7,8,6))

start1 = ((13,2,10,3),
         (1,12,8,4),
         (5,0,9,6),
          (15,14,11,7))
start3 = ((5,1,7,3),
         (9,2,11,4),
         (13,6,15,8),
         (0,10,14,12))

start4 = ((1,2,3,4,5),
          (6,7,8,10,20),
          (11,19,12,0,23),
          (16,22,17,9,14),
          (21,18,15,13,24)
         )
start = start3
row = len(start)-1
col = len(start[0])-1


# In[3]:
################################################
# Goal samples
################################################

goal =          ((1,2,3),
                 (4,5,6),
                 (7,8,0))
goal1 = ((1,2,3,4),
         (5,6,7,8),
         (9,10,11,12),
         (13,14,15,0))

goal2 = ((1,2,3,4,5),
        (6,7,8,9,10),
        (11,12,14,15,20),
         (16,17,19,13,23),
        (21,22,18,0,24))
goal = goal1
goal = (goal,(row,col))


# In[4]:


operations = [(1,0),(0,1),(0,-1),(-1,0)]


# In[5]:
################################################
# Perform the operation 
################################################

def perform(state,op):
    #print state
    pos = state[1]
    state = [list(i) for i in state[0]]
    
    i = pos[0]
    j = pos[1]
    
    x = i+op[0]          # new position
    y = j+op[1]          # new position
    
    if x>row or y> col or x<0 or y<0:
        return False
    
    tmp = state[i][j]
    state[i][j] = state[x][y]
    state[x][y] = tmp
    
    return (tuple([ tuple(i) for i in state]),(x,y))


# In[6]:
################################################
# To find position of zero
################################################

def find_zero_pos(start):
    for i,_ in enumerate(start):
        for j,_ in enumerate(start[i]):
            if start[i][j]==0:
                return (i,j)




# In[7]:
################################################
#  Apply BFS Search
################################################


def BFS(start,goal):
    i=0
    parent = {}
    visited = set()
    Q = Queue()
    pos = find_zero_pos(start)
    
    Q.put((start,pos))
    state = 0
    while not Q.empty():
        i = i+1
        state = Q.get() 
        #print state[0]
        for op in operations:
            successor = perform(state+tuple(),op)
            
            if successor!=False and hash(successor[0]) not in visited:
                
                visited.add(hash(successor[0]))
                parent[successor[0]] = state[0]
                if successor[0]==goal[0]:
                    return parent,i
                Q.put(successor) 
    print "Not Solvable"


# In[8]:
################################################
# Display the grid
################################################


def display(x):
    tm = []
    for i in x:
        if i==0:
            tm.append("*")
        else:
            tm.append(str(i))
    return " ".join(tm)



def BFS_Search():
    parent,i =  BFS(start,goal)
    print "nodes expanded : "+str(i)+"\n"
    
    l = [goal[0]]
    state = goal[0]
    
    
    while state!=start:
        state = parent[state]
        l.append(state)
    
    print "Steps : "+ str(len(l))
    
    while len(l)!=0:
        s = l.pop()
        s = [list(i) for i in s]
        print "---------"
        for x in s:
            print display(x)
    print "--------"    
BFS_Search()




# In[15]:
################################################
# Use DFS search
################################################

def DFS(state,visited,parent,stack,limit,i):
    
    i[0]= i[0]+1
    if i[0]%50000==0:
        print i[0]
    if limit==0:
        return
    visited.add(state)
    
    for op in operations:
            successor = perform(state+tuple(),op)
            if successor!=False and successor not in visited:
                
                parent[successor[0]] = state[0]
                if successor[0]==goal[0]:
                    return goal
                DFS(successor,visited,parent,stack,limit-1,i)
                


# In[16]:


def DFS_Search(start):
    visited = set()
    parent = dict()
    stack = dict()
    depth_limit = 30                   # put a limit here
    i=[0,0]
    
    pos = find_zero_pos(start)
    start = (start,pos)

    DFS(start,visited,parent,stack,depth_limit,i)
    
    print "nodes expanded : "+str(i[0])+"\n"
    l = [goal[0]]
    state = goal[0]
    
    while state!=start[0]:
        state = parent[state]
        l.append(state)
    print "Steps : "+ str(len(l))
    while len(l)!=0:
        s = l.pop()
        s = [list(i) for i in s]
        print "---------"
        for x in s:
            print display(x)
    print "--------"    
    
    
DFS_Search(start)



# In[17]:
################################################
# Use A* ALgorithm
################################################

def h(low,high):
    x1 = low[1][0]
    y1 = low[1][1]
    
    x2 = high[1][0]
    y2 = high[1][1]
    
    #print abs(x2-x1)+abs(y2-y1)
    return abs(x2-x1)+abs(y2-y1)



def A_Star(start,goal):
    
    i=0
    distance = dict()
    parent = dict()
    
    pos = find_zero_pos(start)
    start = (start,pos)
    
    pq = PriorityQueue()
    
    pq.put((0,start))
    distance[start] = 0
    
    while not pq.empty():
        
        i = i+1
        key = pq.get()
        state = key[1]
        w = key[0]
        
        if state[0]==goal[0]:
            return parent,i
            
        for op in operations:
            successor = perform(state+tuple(),op)
            
            if distance.get(successor)==None:
                distance[successor] = int(1e9)
                
            if successor!=False and distance[state]+1+h(goal,successor) < distance[successor]+h(goal,successor):
                
                distance[successor] = distance[state]+1
                
                parent[successor[0]] = state[0]
                pq.put((distance[successor]+h(goal,successor),successor))
    return parent,"Not Solvable"
                


# In[18]:


def AStar_Search():
    
    parent,i = A_Star(start,goal)
    
    print "nodes expanded : "+str(i)+"\n"
    
    l = [goal[0]]
    state = goal[0]
    
    while state!=start:
        state = parent[state]
        l.append(state)

    while len(l)!=0:
        s = l.pop()
        s = [list(i) for i in s]
        print "---------"
        for x in s:
            print display(x)
    print "--------"   
    
AStar_Search()




# In[19]:
################################################
# Use IDA* Algorithm
################################################

parent = []
nodes = 0

def IDFS(limit,f,visited,v):
    global nodes
    nodes = nodes+1
    state = visited[len(visited)-1]
    #print state
    if goal[0]==state[0]:
        global parent
        parent = visited[:]
        return True
    
    if f + h(goal,state) > limit:
        return f + h(goal,state)
    
    fnew = int(1e9)
    
    for op in operations:
            
            successor = perform(state+tuple(),op)
            
            if successor!=False and successor not in v:
                
                visited.append(successor)
                v.add(successor)
                res = IDFS(limit,f + 1,visited,v)
                v.remove(visited.pop())
                if res==True:
                    return res
                if res<fnew:
                    fnew = res
    return fnew 


def IDA_Star(start,goal):
    limit = 0
    global i
    pos = find_zero_pos(start)
    start = (start,pos)
    v = set()
    
    visited = [start]
    res = False
    depth = 10000
    v.add(start)
    
    threshold = h(start,goal)
    
    
    while res!=True:
        res = IDFS(limit,threshold,visited,v)
        print "limit : " + str(limit)
        if res>10000:
            break
        if res==True:
            break
        limit = res
        
    print "nodes expanded : "+str(nodes)+"\n"
        
    for s in parent:
        s = s[0]
        s = [list(i) for i in s]
        print "---------"
        for x in s:
            print display(x)
        print "---------"
     
    

IDA_Star(start,goal)
    
    
    
    


# ##  ===============             SECOND_PART           ===========================

# In[20]:


start = ((1,1,1,1),
         (2,2,2,2),
         (3,3,3,3),
         (4,4,4,4))

start1 = ((1,1,1),
         (1,2,2),
         (2,2,2))
start2 = ((1,1,1,1),
         (1,1,1,1),
         (2,2,2,2),
         (2,2,2,2))
start = start2
row = len(start)-1
col = len(start[0])-1
start = (start,(0,0))
start


# In[23]:


def check(x,y):
    if x>row or y> col or x<0 or y<0:
        return False
    else:
        return True
    

def is_goal(state):
    
    operation = [(1,0),(0,1),(0,-1),(-1,0)]
    #print state
    for i in range(0,len(state)):
        for j in range(0,len(state[i])):
            
            for op in operation:
                x = i+op[0]          
                y = j+op[1]
                
                if check(x,y) and state[x][y]==state[i][j]:
                    return False
    return True


# In[24]:
################################################
# Generate neighboring states
################################################

def generate(state):
    
    pos = state[1]
    
    i = pos[0]
    j = pos[1]
    
    if j+1<=col:
        x = 0
        y = j+1
    else:
        x = i+1
        y = 0    
    
    if x>row or y>col:
        pos = False
    else:
        pos = (x,y)
    #print pos
    successors = [(state[0],pos)]
    
    state = [list(w) for w in state[0]]
    
    
    for r in range(i,len(state)):
        for c in range(j,len(state[r])):
            
            s = copy.deepcopy(state)
            
            if state[i][j]==state[r][c]:
                continue
            else:
                
                tmp  = s[i][j]
                s[i][j] = s[r][c]
                s[r][c] = tmp

                m = (tuple([tuple(w) for w in s]),pos)
                #print m
                successors.append(m)
                
            
    return successors        
    


# In[25]:


#generate((start[0],(0,0)))


# In[28]:



memory = 0

def BFS_2(start):
    global memory
    i = 0
    parent = {}
    
    Q = Queue()
    
    Q.put(start)
    
    while not Q.empty():
        i = i+1
        
        state = Q.get()
        
        size = sys.getsizeof(Q)
        if size>memory:
            memory = size
        
        if state[1]==False:
                continue
            
        successor_states = generate(state)
        
        for successor in successor_states:
            
            parent[successor[0]] = state[0]
            
            if is_goal(successor[0]):
                print "Total Memory taken by Queue : " +str(memory)
                return parent,i,successor[0]
            Q.put(successor)
    return False,i,str("N")    
        


# In[29]:


def BFS2_Search():
    #start = (((1, 1, 2), (1, 2, 1), (2, 2, 2)), (0, 0))
    parent,i,goal =  BFS_2(start)
    print "nodes expanded : "+str(i)
    for x in goal:
        print list(x)
        
    state = goal

    
BFS2_Search()


# ## ===============   DFS  =============

# In[30]:
################################################
# DFS Driver
################################################

nodes = 0
parent = {}
solution = 0

def DFS_2(state,limit):
    global nodes,parent,solution
    
    if state[1]== False :
        return
    
    
    if limit==0:
        return 
    
    successor_nodes = generate(state)
    
    for successor in successor_nodes:
        parent[successor[0]] = state[0]
        nodes = nodes + 1
        if is_goal(successor[0]):
            solution = successor[0]
            return
        
        DFS_2(successor,limit-1)
        

def DFS2_Search():
    limit = 9
    DFS_2(start,limit)
    print "nodes expanded : "+str(nodes)
    
    print "Sizeof "+str(sys.getsizeof(parent))
    if solution==0:
        print "Not possible"
        return
    for x in solution:
        print list(x)
DFS2_Search()
    

