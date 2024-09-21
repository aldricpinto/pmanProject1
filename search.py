# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # (successor,action, stepCost) -> getSuccessors
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    finalActionList = []
    
    #Fringe representation used is : 'Stack'
    stackForDfs = util.Stack()
    
    
    stackForDfs.push((problem.getStartState(),finalActionList))
    # print('Initial State of Stack : ',stackForDfs.list)
    
    # using a closedSet to maintain a track of nodes that have already been visited
    closedSet = set()
    
    while not stackForDfs.isEmpty():
        lastInFirstOutState,actionList = stackForDfs.pop()
        # print('Popped: ', lastInFirstOutState)
        
        if problem.isGoalState(lastInFirstOutState):
            return actionList
        
        if lastInFirstOutState in closedSet:
            continue
            
        closedSet.add(lastInFirstOutState)
            # print('In closedSet : ',closedSet)
        
        successorsList = problem.getSuccessors(lastInFirstOutState)
        
        for successor,action, stepCost in successorsList:
            # print('successor',successor)
            if not successor in closedSet:
                initialPath = actionList
                # print('action',action)
                # print('initialPath',initialPath)
                sucessorPath = [action]
                # print('sucessorPath',sucessorPath)
                
                updatedPath = [*initialPath,*sucessorPath] 
                stackForDfs.push((successor,updatedPath))
                # print('updatedPath',updatedPath)
                # print('successor',successor)
                
    util.raiseNotDefined()
    return finalActionList
            
            

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    finalActionList = []
    
    # Fringe representation used for BFS : 'Queue'
    QueueForBfs = util.Queue()
    
    
    QueueForBfs.push((problem.getStartState(),finalActionList))
    
    # print('Initial State of Queue : ',QueueForBfs.list)
    closedSet = set()
    
    while not QueueForBfs.isEmpty():
        firstInFirstOutState,actionList = QueueForBfs.pop()
        # print('Popped: ', firstInFirstOutState)
        
        if problem.isGoalState(firstInFirstOutState):
            return actionList

        if  firstInFirstOutState in closedSet:
            continue
        
        closedSet.add(firstInFirstOutState)
            
        successorsList = problem.getSuccessors(firstInFirstOutState)
        
        # print(QueueForBfs.list)
        
        
        for successor,action, stepCost in successorsList:

            if not successor in closedSet:
                initialPath = actionList
                sucessorPath = [action]
                updatedPath = [*initialPath,*sucessorPath] 
                QueueForBfs.push((successor,updatedPath))
                
    util.raiseNotDefined()
    return finalActionList
    

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    finalActionList = []
    
    #Fringe representation for UCS used is : 'PriorityQueue'
    pqueueForUCS = util.PriorityQueue()
    pqueueForUCS.push((problem.getStartState(),finalActionList),0)
    closedSet = set()
    
    
    
    while not pqueueForUCS.isEmpty():
        cheapestState,actionList = pqueueForUCS.pop()


        if problem.isGoalState(cheapestState):
            return actionList

        if cheapestState in closedSet:
            continue
        
        closedSet.add(cheapestState)
               
        successorsList = problem.getSuccessors(cheapestState)
        # print('This is heap: ',pqueueForUCS.heap)
        # As seen from util that priority queue stores [cost,count,stateActionListTuple]
        checkingStateinPrQueueForUcs = [stateAndActions[0] for cost,count,stateAndActions in pqueueForUCS.heap]

        for successor,action, stepCost in successorsList:

            if not successor in closedSet :
                
                initialPath = actionList
                sucessorPath = [action]
                updatedPath = [*initialPath,*sucessorPath] 
                
                updatedCost = problem.getCostOfActions(updatedPath)
                
                pqueueForUCS.push((successor,updatedPath),updatedCost)
                
            
                    
                
    
    
    util.raiseNotDefined()
    return finalActionList



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    finalActionList = []
    
    # Fringe representation for A* used is : 'PriorityQueue'
    pqueueForAstar = util.PriorityQueue()
    
    
    pqueueForAstar.push((problem.getStartState(),finalActionList),heuristic)
    closedSet = set()
    
    
    
    while not pqueueForAstar.isEmpty():
        cheapestState,actionList = pqueueForAstar.pop()


        if problem.isGoalState(cheapestState):
            return actionList

        if cheapestState in closedSet:
            continue
        
        closedSet.add(cheapestState)    
            
        successorsList = problem.getSuccessors(cheapestState)
        
        for successor,action, stepCost in successorsList:
            if not successor in closedSet :
                
                initialPath = actionList
                sucessorPath = [action]
                updatedPath = [*initialPath,*sucessorPath] 
                
                gofn = problem.getCostOfActions(updatedPath)
                fofn = gofn + heuristic(successor,problem)
                
                pqueueForAstar.push((successor,updatedPath),fofn)
            
            
    util.raiseNotDefined()            
    return finalActionList
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
