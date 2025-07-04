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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # print(legalMoves)

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # print(scores)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # print(bestIndices)
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        
        # print(legalMoves[chosenIndex])
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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

        foodlist = newFood.asList()
        mindisghost = 999999
        for ghostState in newGhostStates:
            ghost = ghostState.getPosition()
            # print("test", ghost, newPos)
            if manhattanDistance(ghost, newPos) <= 1:
                # print("test")
                return 0
            mindisghost = min(mindisghost, manhattanDistance(ghost, newPos))
        mindisfood = 999999
        for food in foodlist:
            mindisfood = min(mindisfood, manhattanDistance(food, newPos))
        for food in currentGameState.getFood().asList():
            if food == newPos:
                mindisfood = -999999
        
        # print(1 / mindisghost)
        return 999999 - mindisfood - 1 / mindisghost 

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        def dfs(gameState: GameState, depth, agentIndex):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), Directions.STOP
            num = gameState.getNumAgents()
            lessdep = 1 if agentIndex + 1 == num else 0
            if agentIndex == 0:
                maxx = -999999
                maxdirection = Directions.STOP
                for action in gameState.getLegalActions(agentIndex):
                    val, direction = dfs(gameState.generateSuccessor(agentIndex, action), depth - lessdep, (agentIndex + 1) % num)
                    if val > maxx:
                        maxx = val
                        maxdirection = action
                return maxx, maxdirection
            else:
                minx = 999999
                mindirection = Directions.STOP
                for action in gameState.getLegalActions(agentIndex):
                    val, direction = dfs(gameState.generateSuccessor(agentIndex, action), depth - lessdep, (agentIndex + 1) % num)
                    if val < minx:
                        minx = val
                        mindirection = action
                return minx, mindirection

        val, action = dfs(gameState, self.depth, 0)
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        def dfs(gameState: GameState, depth, agentIndex, alpha, beta):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), Directions.STOP
            num = gameState.getNumAgents()
            lessdep = 1 if agentIndex + 1 == num else 0
            if agentIndex == 0:
                maxx = -999999
                maxdirection = Directions.STOP
                for action in gameState.getLegalActions(agentIndex):
                    val, direction = dfs(gameState.generateSuccessor(agentIndex, action), depth - lessdep, (agentIndex + 1) % num, alpha, beta)
                    if val > maxx:
                        maxx = val
                        maxdirection = action
                    if val > beta:
                        return val, action
                    alpha = max(alpha, val)
                return maxx, maxdirection
            else:
                minx = 999999
                mindirection = Directions.STOP
                for action in gameState.getLegalActions(agentIndex):
                    val, direction = dfs(gameState.generateSuccessor(agentIndex, action), depth - lessdep, (agentIndex + 1) % num, alpha, beta)
                    if val < minx:
                        minx = val
                        mindirection = action
                    if val < alpha:
                        return val, action
                    beta = min(beta, val)
                return minx, mindirection

        val, action = dfs(gameState, self.depth, 0, -999999, 999999)
        return action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def dfs(gameState: GameState, depth, agentIndex):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), Directions.STOP
            num = gameState.getNumAgents()
            lessdep = 1 if agentIndex + 1 == num else 0
            if agentIndex == 0:
                maxx = -999999
                maxdirection = Directions.STOP
                for action in gameState.getLegalActions(agentIndex):
                    val, direction = dfs(gameState.generateSuccessor(agentIndex, action), depth - lessdep, (agentIndex + 1) % num)
                    if val > maxx:
                        maxx = val
                        maxdirection = action
                return maxx, maxdirection
            else:
                sum = 0
                cnt = 0
                mindirection = Directions.STOP
                for action in gameState.getLegalActions(agentIndex):
                    val, direction = dfs(gameState.generateSuccessor(agentIndex, action), depth - lessdep, (agentIndex + 1) % num)
                    sum += val
                    cnt += 1
                return sum / cnt, Directions.STOP

        val, action = dfs(gameState, self.depth, 0)
        return action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodlist = newFood.asList()
    # mindisghost = 999999
    # for ghostState in newGhostStates:
    #     ghost = ghostState.getPosition()
    #     if manhattanDistance(ghost, newPos) <= 1:
    #         return -999999
    #     mindisghost = min(mindisghost, manhattanDistance(ghost, newPos))
    mindisfood = 999999 if len(foodlist) != 0 else -999999
    for food in foodlist:
        mindisfood = min(mindisfood, manhattanDistance(food, newPos))
    # for food in currentGameState.getFood().asList():
    #     if food == newPos:
    #         mindisfood = -999999
    
    import random

    return 999999 - random.uniform(0.9, 1) * mindisfood - 10 * len(foodlist) + currentGameState.getScore() * 2 - 100 * len(currentGameState.getCapsules())

# Abbreviation
better = betterEvaluationFunction
