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
    
    # Initialising Fringe representation : 'Stack'
    stackForDfs = util.Stack()
    
    # actionMap to maintain a map of 'states' and the 'action' (i.e direction : N,S,E,W etc) as a List which will be returned 
    # when a goal state is achieved.
    
    actionMap = {problem.getStartState():[]}
    print('This is actionMap keys: ',actionMap.keys())
    stackForDfs.push(problem.getStartState())
    print('Initial State of Stack : ',stackForDfs.list)
    
    # using a closedSet to maintain a track of nodes that have already been visited
    closedSet = set()
    
    while not stackForDfs.isEmpty():
        lastInFirstOutState = stackForDfs.pop()
        # print('Popped: ', lastInFirstOutState)
        
        if problem.isGoalState(lastInFirstOutState):
            finalActionList = actionMap[lastInFirstOutState]
            # print(finalActionList)
            return finalActionList
        
        if not lastInFirstOutState in closedSet:
            
            closedSet.add(lastInFirstOutState)
            # print('In closedSet : ',closedSet)
        
        successorsList = problem.getSuccessors(lastInFirstOutState)
        
        for successor,action, stepCost in successorsList:
            # print('at actionMap : ',actionMap)
            # print('successor',successor)
            if not successor in closedSet:
                stackForDfs.push(successor)
                initialPath = actionMap[lastInFirstOutState]
                # print('action',action)
                # print('initialPath',initialPath)
                sucessorPath = [action]
                # print('sucessorPath',sucessorPath)
                
                updatedPath = [*initialPath,*sucessorPath] 
                
                # print('updatedPath',updatedPath)
                # print('successor',successor)
                
                actionMap[successor]=updatedPath
                # print('at actionMap inside if : ',actionMap)
                
    util.raiseNotDefined()
    return finalActionList
            
            

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    finalActionList = []
    
    # Initialising Fringe representation : 'Queue'
    QueueForBfs = util.Queue()
    
    # actionMap to maintain a map of 'states' and the 'action' (i.e direction : N,S,E,W etc) as a List which will be returned 
    # when a goal state is achieved.
    
    
    actionMap = {problem.getStartState():[]}
    print('This is actionMap keys: ',actionMap.keys())
    QueueForBfs.push(problem.getStartState())
    print('Initial State of Queue : ',QueueForBfs.list)
    closedSet = set()
    closedSet.add(problem.getStartState())
    
    while not QueueForBfs.isEmpty():
        firstInFirstOutState = QueueForBfs.pop()
        # print('Popped: ', firstInFirstOutState)
        if problem.isGoalState(firstInFirstOutState):
            finalActionList = actionMap[firstInFirstOutState]
            # print(finalActionList)
            return finalActionList
        
        successorsList = problem.getSuccessors(firstInFirstOutState)
        
        for successor,action, stepCost in successorsList:
            # print('at actionMap : ',actionMap)
            # print('successor',successor)
            if not successor in closedSet:
                closedSet.add(successor)
                QueueForBfs.push(successor)
                initialPath = actionMap[firstInFirstOutState]
                # print('action',action)
                # print('initialPath',initialPath)
                sucessorPath = [action]
                # print('sucessorPath',sucessorPath)
                updatedPath = [*initialPath,*sucessorPath] 
                # print('updatedPath',updatedPath)
                # print('successor',successor)
                actionMap[successor]=updatedPath
                # print('at actionMap inside if : ',actionMap)
                
    util.raiseNotDefined()
    return finalActionList
    

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    finalActionList = []
    
    # Initialising Fringe representation : 'PriorityQueue'
    pqueueForUCS = util.PriorityQueue()
    
    # actionMap to maintain a map of 'states' and the 'action' (i.e direction : N,S,E,W etc) as a List which will be returned 
    # when a goal state is achieved.
    actionMap = {problem.getStartState():[]}
    pqueueForUCS.push(problem.getStartState(),0)
    closedSet = set()
    
    closedSet.add(problem.getStartState())
    
    
    while not pqueueForUCS.isEmpty():
        cheapestState = pqueueForUCS.pop()


        if problem.isGoalState(cheapestState):
            finalActionList = actionMap[cheapestState]
            return finalActionList

            
        successorsList = problem.getSuccessors(cheapestState)
        
        for successor,action, stepCost in successorsList:
            if not successor in closedSet:
                closedSet.add(successor)
                initialPath = actionMap[cheapestState]
                sucessorPath = [action]
                updatedPath = [*initialPath,*sucessorPath] 
                
                updatedCost = problem.getCostOfActions(updatedPath)
                
                pqueueForUCS.push(successor,updatedCost)
                
                actionMap[successor]=updatedPath
    
    
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
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
