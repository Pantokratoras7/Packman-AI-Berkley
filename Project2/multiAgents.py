# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # Find the distance of ghosts from pacman after moving in the new Position
        # Distance is found using the manhattan algorithm (util.py by default)
        # Then find the minimum distance from this list of distances
        ghostList = []
        for ghostState in newGhostStates:
            ghostList.append(manhattanDistance(newPos, ghostState.getPosition()))
        nearestGhostDistance = min(ghostList)

        # Initialize the evaluation variable as the successor's score (proposed next state)
        # If score is better in a possible move, apparrently that is a desirable situation
        # Usually, better score means that pacman eating food
        # Better score means bigger value for evalDistance (better)
        evalDistance = scoreEvaluationFunction(successorGameState)

        # If a ghost is near, then follow it, as most of the times goes throughout the grid
        # There is no need of worring, as if the successor state is lose, evalDistance will be very low
        # For this reason, the move towards defeat will never be prefered (except rare situations)
        # In autograder, this evaluation function has very good scores and wins 9 of 10 times
        # Apparently, this one defeat is due to an extreme situation that I cannot predict
        if nearestGhostDistance < 3:
            evalDistance += nearestGhostDistance

        return evalDistance
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        self.ghosts = gameState.getNumAgents() - 1          # Number of ghosts (1 agent is the player (0), the rest are ghosts)
        move = self.maxValue(gameState, 0, self.index, 1)   # Minimax-Decision function in Minimax algorithm is just like maxValue
        return move                                         # The only difference is that returns the action instead of a utility value
        util.raiseNotDefined()

    def maxValue(self, state, depth, agent=0, start=0):                 # In maxValue function default agent is 0 (pacman)
        bestAction = None
        if state.isWin() or state.isLose() or depth == self.depth:      # If this is a win or lose state return an evaluated number
            return self.evaluationFunction(state)                       # Also, if this is maximum depth, then this state is a leaf
        n = -float('Inf')                                               # Initialize the n variable as minus infinity
        legalActions = state.getLegalActions(agent)
        for action in legalActions:
            result = state.generateSuccessor(agent, action)             # Generate a successor state for every legal move
            prevn = n
            n = max(n, self.minValue(result, depth, agent+1))           # Find the maximum min-value (min nodes symbolize ghosts)
            if (n > prevn):
                bestAction = action                                     # Keep the best action to return if the above node is root
        if start == 0:
            return n                                                    # Return either the n value or the action if the parent is root
        else:
            return bestAction

    def minValue(self, state, depth, agent):
        if state.isWin() or state.isLose() or depth == self.depth:      # More of the same as above
            return self.evaluationFunction(state)
        n = float('Inf')
        legalActions = state.getLegalActions(agent)
        for action in legalActions:
            result = state.generateSuccessor(agent, action)
            if (agent < self.ghosts):
                n = min(n, self.minValue(result, depth, agent+1))       # If there are more ghosts, then examine them calling minValue
            else:
                n = min(n, self.maxValue(result, depth+1))              # If not, check the next possible moves of pacman
        return n



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        self.ghosts = gameState.getNumAgents() - 1                      # Alpha-Beta is very similar to Minimax algorithm
        a = -float('Inf')                                               # As a result we have almost the same code and principles
        b = float('Inf')                                                # We simply add alpha, beta values and the needed comparisons
        move = self.maxValue(gameState, a, b, 0, self.index, 1)         # Consequently, more explanation is unnecessary
        return move
        util.raiseNotDefined()

    def maxValue(self, state, alpha, beta, depth, agent=0, start=0):
        bestAction = None
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        n = -float('Inf')
        legalActions = state.getLegalActions(agent)
        for action in legalActions:
            result = state.generateSuccessor(agent, action)
            prevn = n
            n = max(n, self.minValue(result, alpha, beta, depth, agent+1))
            if (n > prevn):
                bestAction = action
            if n > beta:
                return n
            alpha = max(n, alpha)
        if start == 0:
            return n
        else:
            return bestAction

    def minValue(self, state, alpha, beta, depth, agent):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        n = float('Inf')
        legalActions = state.getLegalActions(agent)
        for action in legalActions:
            result = state.generateSuccessor(agent, action)
            if (agent < self.ghosts):
                n = min(n, self.minValue(result, alpha, beta, depth, agent+1))
            else:
                n = min(n, self.maxValue(result, alpha, beta, depth+1))
            if n < alpha:
                return n
            beta = min(n, beta)
        return n



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        self.ghosts = gameState.getNumAgents() - 1                          # Expectimax algorithm, follows more of the same principles
        move = self.maxValue(gameState, 0, self.index, 1)
        return move
        util.raiseNotDefined()

    def maxValue(self, state, depth, agent=0, start=0):                     # MaxValue is exactly the same as the one in Minimax
        bestAction = None
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        n = -float('Inf')
        legalActions = state.getLegalActions(agent)
        for action in legalActions:
            result = state.generateSuccessor(agent, action)
            prevn = n
            n = max(n, self.expValue(result, depth, agent+1))
            if (n > prevn):
                bestAction = action
        if start == 0:
            return n
        else:
            return bestAction

    def expValue(self, state, depth, agent):                                # ExpValue is the replacement of minValue for chance nodes
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        n = 0                                                               # Here, instead of initializing as infinity use 0
        legalActions = state.getLegalActions(agent)
        expectation = 1.0/len(legalActions)                                 # The expectation for each child node is the same
        for action in legalActions:
            result = state.generateSuccessor(agent, action)
            if (agent < self.ghosts):
                n += self.expValue(result, depth, agent+1)*expectation      # For every child (pacman or ghost) calculate its value
            else:                                                           # Returned value is multiplied by its expectation
                n += self.maxValue(result, depth+1)*expectation             # Chance node's value is the summary of the above
        return n



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    pacmanPos = currentGameState.getPacmanPosition()                        # Find the current pacman position
    foodGrid  = currentGameState.getFood()                                  # Get the table's food in a grid
    ghostGrid = currentGameState.getGhostPositions()                        # Get ghosts' positions

    # If this state is winning, be sure this is the the maximum node
    # If is losing, then we have to avoid it!!
    if currentGameState.isWin():
        return 1000000
    if currentGameState.isLose():
        return -1000000

    # Find the minimum ghost distance from this state, using manhattan algorithm (just like ReflexAgent)
    ghostList = []
    for ghostPosition in ghostGrid:
        ghostList.append(manhattanDistance(pacmanPos, ghostPosition))
    nearestGhostDistance = min(ghostList)

    # In the same way, find the minimum distance from food
    foodList = []
    for foodDistance in foodGrid.asList():
        foodList.append(manhattanDistance(pacmanPos, foodDistance))
    nearestFoodDistance = min(foodList)

    # We initialize evalDistance as the current score, as for better total score higher value will be returned
    # For example, 2 neighbor states may have similar distances from ghosts and food, but due to better score one would be preffered
    evalDistance = scoreEvaluationFunction(currentGameState)

    # Higher ghost distance is better, so the state which is nearest to a ghost will return lowest value
    # Lower food distance is better, so subtracting lower distances is better for evalDistance
    evalDistance += nearestGhostDistance                                                                # Ghost - Add
    evalDistance -= nearestFoodDistance                                                                 # Food - Subtract

    return evalDistance

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

