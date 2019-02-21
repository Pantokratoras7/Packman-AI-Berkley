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


# A class for the each node as presented in the lecture
class GraphNode():
    def __init__(self, state, parent, action, pathCost):
        self.state    = state
        self.parent   = parent
        self.action   = action
        self.pathCost = pathCost



def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]



def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    node = GraphNode(problem.getStartState(), None, None, 0)		# Initialize a root node
    frontier = util.Stack()											# Create a stack for fringe in DFS
    frontier.push(node)
    explored = set()

    while 1:										# Exactly the same algorithm as the one in lectures

        if frontier.isEmpty():
            return None
        node = frontier.pop()						# Examine the fringe node

        if problem.isGoalState(node.state):			# Check if this is our goal
            path = []
            while node.parent is not None:			# If so, record the path from root to goal
                path.append(node.action)
                node = node.parent
            path = path[::-1]						# We have to reverse it as we read it backwards
            return path

        explored.add(node.state)					# Add an the node to the explored ones

        successor = problem.getSuccessors(node.state)		# Find all the possible children
        for nextState, action, cost in successor:
            child = GraphNode(nextState, node, action, node.pathCost+cost)		# And initialize them

            if child.state not in explored:
                if child.state not in frontier.list:		# If the child's position is no explored nor a frontier 
                    frontier.push(child)					# Add it to fringe (look for the state only)

    util.raiseNotDefined()



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    node = GraphNode(problem.getStartState(), None, None, 0)
    frontier = util.Queue()											# Create a queue for fringe in DFS
    frontier.push(node)
    explored = set()
    visited  = set()						# Add one more set, to keep all the states we have met
    visited.add(node.state)					# As the frontier stack changes, and we may check again nodes checked before

    while 1:

        if frontier.isEmpty():
            return None
        node = frontier.pop()
        #print node.state

        if problem.isGoalState(node.state):			# I chose to implement slightly differently the BFS check for goal state
            path = []								# I implemented that through the old way, mostl due to autograder
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path = path[::-1]
            return path

        explored.add(node.state)									# The rest are pretty much the same as above

        successor = problem.getSuccessors(node.state)
        for nextState, action, cost in successor:
            child = GraphNode(nextState, node, action, node.pathCost+cost)

            if child.state not in explored:
                if child.state not in visited:
                    frontier.push(child)
                    visited.add(child.state)

    util.raiseNotDefined()



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    node = GraphNode(problem.getStartState(), None, None, 0)
    frontier = util.PriorityQueue()									# Create a priority queue for UCS
    frontier.push(node, node.pathCost)
    explored = set()
    visited  = set()
    visited.add(node.state)					# Add visited set once more

    while 1:

        if frontier.isEmpty():
            return None
        node = frontier.pop()
        #print node.state

        if problem.isGoalState(node.state):				# The basic implementations are same as the previous ones
            path = []
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path = path[::-1]
            return path

        explored.add(node.state)

        successor = problem.getSuccessors(node.state)
        for nextState, action, cost in successor:
            if nextState not in explored:
                child = GraphNode(nextState, node, action, node.pathCost+cost)

                if child.state not in visited:
                    visited.add(child.state)						# Implement the code in this part according to the lectures
                    frontier.push(child, child.pathCost)
                else:												# I don't use the update function as can use already checked nodes
                    tuples = []
                    for tuples in frontier.heap:					# To avoid repeated checks of nodes, we copy their values for updating
                        if tuples[2].state == child.state:
                            if tuples[2].pathCost > child.pathCost:
                                tuples[2].state = child.state
                                tuples[2].pathCost = child.pathCost
                                tuples[2].parent = child.parent
                                tuples[2].action = child.action

    util.raiseNotDefined()



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    node = GraphNode(problem.getStartState(), None, None, 0)
    frontier = util.PriorityQueue()									# Create a priority queue in A-Star, like in UCS
    frontier.push(node, 0)
    explored = set()
    visited  = set()
    visited.add(node.state)

    while 1:

        if frontier.isEmpty():
            return None
        node = frontier.pop()
        #print node.state

        if problem.isGoalState(node.state):				# The basic parts of algorithm are similar (graph-algorithm)
            path = []
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path = path[::-1]
            #print explored
            return path

        if node.state not in explored:					# Although, the main difference from the previous is the explored nodes
            explored.add(node.state)					# We have to check them before adding a new one in the explored set
            #print node.state 							# It is slightly different from lecture's algorithm, but works only in this way

            successor = problem.getSuccessors(node.state)
            for nextState, action, cost in successor:
            #if nextState not in explored:
                child = GraphNode(nextState, node, action, node.pathCost+cost)
                new_cost = child.pathCost + heuristic(child.state, problem)     # Calculate the new cost of path using heuristic function

                if child.state not in visited:
                    #print child.state
                    visited.add(child.state)
                    frontier.push(child, new_cost)				# we use visited set to check duplicates as in the UCS
                else:
                    tuples = []
                    for tuples in frontier.heap:
                        if tuples[2].state == child.state:
                            if tuples[2].pathCost > child.pathCost:
                                tuples[2].state = child.state
                                tuples[2].pathCost = child.pathCost
                                tuples[2].parent = child.parent
                                tuples[2].action = child.action
                        else:										# However, now we use update, as A* must reassign nodes' priority
                            frontier.update(child, new_cost)		# As this is done in a more complex way (works this way!!)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
