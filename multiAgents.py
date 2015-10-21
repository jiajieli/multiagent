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
        legalMoves = currentGameState.getLegalActions()
        gPosition = successorGameState.getGhostPositions()
        pPosition = currentGameState.getPacmanPosition()
        foodList = currentGameState.getFood().asList()
        if len(foodList) == 0:
          return 10000
        score = 0
        if successorGameState.hasWall(newPos[0], newPos[1]+1) and successorGameState.hasWall(newPos[0], newPos[1]-1) and successorGameState.hasWall(newPos[0]+1, newPos[1]):
          score -= 100
        if successorGameState.hasWall(newPos[0], newPos[1]+1) and successorGameState.hasWall(newPos[0], newPos[1]-1) and successorGameState.hasWall(newPos[0]-1, newPos[1]):
          score -= 100
        if successorGameState.hasWall(newPos[0]+1, newPos[1]) and successorGameState.hasWall(newPos[0]-1, newPos[1]) and successorGameState.hasWall(newPos[0], newPos[1]+1):
          score -= 100
        if successorGameState.hasWall(newPos[0]+1, newPos[1]) and successorGameState.hasWall(newPos[0]-1, newPos[1]) and successorGameState.hasWall(newPos[0], newPos[1]-1):
          score -= 100
        for i in gPosition:
          dis = util.manhattanDistance(newPos, i)
          if newScaredTimes[0] < 1:
            if dis < 2:
              return -99999
            elif dis < 4:
              score+=dis
        nextDistanceToFurthestFood = (util.manhattanDistance(newPos, foodList[0]))
        if newPos in foodList:
          score += 10
        else:
          currentDistanceToFurthestFood = (util.manhattanDistance(pPosition, foodList[0]))
          if nextDistanceToFurthestFood == currentDistanceToFurthestFood:
            score -= (5*(legalMoves.index(action)+1))
        score-=nextDistanceToFurthestFood
        return score+10000.0/(len(foodList)+1)

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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.value(gameState, 0)[0]

    def value(self, gameState, index):
      if index % gameState.getNumAgents() == 0:
        return self.max_value(gameState, index)
      else:
        return self.min_value(gameState, index)

    def max_value(self, gameState, index):
      actions = gameState.getLegalActions(self.index) #self.index is 0 always
      if len(actions) == 0:
        return ('', self.evaluationFunction(gameState))
      bestActionPair = (actions[0], -100000)
      if index / gameState.getNumAgents() >= self.depth or gameState.isWin() or gameState.isLose():
        return (bestActionPair[0], self.evaluationFunction(gameState))
      for act in actions:
        successorState = gameState.generateSuccessor(self.index, act)
        successorActionPair = self.value(successorState, index+1)
        if successorActionPair[1] >= bestActionPair[1]:
          bestActionPair = (act, successorActionPair[1])
      return bestActionPair

    def min_value(self, gameState, index):
      actions = gameState.getLegalActions(index % gameState.getNumAgents())
      if len(actions) == 0:
        return ('', self.evaluationFunction(gameState))
      bestActionPair = (actions[0], 100000)
      if index / gameState.getNumAgents() >= self.depth or gameState.isWin() or gameState.isLose():
        return (bestActionPair[0], self.evaluationFunction(gameState))
      for act in actions:
        successorState = gameState.generateSuccessor(index % gameState.getNumAgents(), act)
        successorActionPair = self.value(successorState, index+1)
        if successorActionPair[1] <= bestActionPair[1]:
          bestActionPair = (act, successorActionPair[1])
      return bestActionPair



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.value(gameState, 0, -100000, +100000)[0]


    def value(self, gameState, index, alpha, beta):
      if index % gameState.getNumAgents() == 0:
        return self.max_value(gameState, index, alpha, beta)
      else:
        return self.min_value(gameState, index, alpha, beta)

    def max_value(self, gameState, index, alpha, beta):
      actions = gameState.getLegalActions(self.index) #self.index is 0 always
      if len(actions) == 0:
        return ('', self.evaluationFunction(gameState))
      bestActionPair = (actions[0], -100000)
      if index / gameState.getNumAgents() >= self.depth or gameState.isWin() or gameState.isLose():
        return (bestActionPair[0], self.evaluationFunction(gameState))
      for act in actions:
        successorState = gameState.generateSuccessor(self.index, act)
        successorActionPair = self.value(successorState, index+1, alpha, beta)
        if successorActionPair[1] >= bestActionPair[1]:
          bestActionPair = (act, successorActionPair[1])
        if bestActionPair[1] > beta:
          return bestActionPair
        alpha = max(alpha, bestActionPair[1])
      return bestActionPair

    def min_value(self, gameState, index, alpha, beta):
      actions = gameState.getLegalActions(index % gameState.getNumAgents())
      if len(actions) == 0:
        return ('', self.evaluationFunction(gameState))
      bestActionPair = (actions[0], 100000)
      if index / gameState.getNumAgents() >= self.depth or gameState.isWin() or gameState.isLose():
        return (bestActionPair[0], self.evaluationFunction(gameState))
      for act in actions:
        successorState = gameState.generateSuccessor(index % gameState.getNumAgents(), act)
        successorActionPair = self.value(successorState, index+1, alpha, beta)
        if successorActionPair[1] <= bestActionPair[1]:
          bestActionPair = (act, successorActionPair[1])
        if bestActionPair[1] < alpha:
          return bestActionPair
        beta = min(beta, bestActionPair[1])
      return bestActionPair

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
        return self.value(gameState, 0)[0]

    def value(self, gameState, index):
      if index % gameState.getNumAgents() == 0:
        return self.max_value(gameState, index)
      else:
        return self.min_value(gameState, index)

    def max_value(self, gameState, index):
      actions = gameState.getLegalActions(self.index) #self.index is 0 always
      if len(actions) == 0:
        return ('', self.evaluationFunction(gameState))
      bestActionPair = (actions[0], -100000)
      if index / gameState.getNumAgents() >= self.depth or gameState.isWin() or gameState.isLose():
        return (bestActionPair[0], self.evaluationFunction(gameState))
      for act in actions:
        successorState = gameState.generateSuccessor(self.index, act)
        successorActionPair = self.value(successorState, index+1)
        if successorActionPair[1] >= bestActionPair[1]:
          bestActionPair = (act, successorActionPair[1])
      return bestActionPair

    def min_value(self, gameState, index):
      actions = gameState.getLegalActions(index % gameState.getNumAgents())
      if len(actions) == 0:
        return ('', self.evaluationFunction(gameState))
      if index / gameState.getNumAgents() >= self.depth or gameState.isWin() or gameState.isLose():
        return (bestActionPair[0], self.evaluationFunction(gameState))
      runningSum = 0
      for act in actions:
        successorState = gameState.generateSuccessor(index % gameState.getNumAgents(), act)
        successorActionPair = self.value(successorState, index+1)
        runningSum += successorActionPair[1]
      return (actions[0], runningSum*1.0/len(actions))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    legalMoves = currentGameState.getLegalActions()
    gStates = currentGameState.getGhostStates()
    gPosition = currentGameState.getGhostPositions()
    scaredTimes = [ghostState.scaredTimer for ghostState in gStates]
    pPosition = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    if len(foodList) == 0:
      return 10000
    score = 0
    if currentGameState.hasWall(pPosition[0], pPosition[1]+1) and currentGameState.hasWall(pPosition[0], pPosition[1]-1) and currentGameState.hasWall(pPosition[0]+1, pPosition[1]):
      score -= 100
    if currentGameState.hasWall(pPosition[0], pPosition[1]+1) and currentGameState.hasWall(pPosition[0], pPosition[1]-1) and currentGameState.hasWall(pPosition[0]-1, pPosition[1]):
      score -= 100
    if currentGameState.hasWall(pPosition[0]+1, pPosition[1]) and currentGameState.hasWall(pPosition[0]-1, pPosition[1]) and currentGameState.hasWall(pPosition[0], pPosition[1]+1):
      score -= 100
    if currentGameState.hasWall(pPosition[0]+1, pPosition[1]) and currentGameState.hasWall(pPosition[0]-1, pPosition[1]) and currentGameState.hasWall(pPosition[0], pPosition[1]-1):
      score -= 100
    for i in gPosition:
      dis = util.manhattanDistance(pPosition, i)
      if scaredTimes[0] < 1:
        if dis < 2:
          return -9999
        # elif dis < 4:
        #   score+=dis*2
    minDis = 10000
    for i in foodList:
      minDis = min(minDis, util.manhattanDistance(pPosition, i))
    return score+5000.0/(len(foodList)+1)-minDis+10*scaredTimes[0]-100*len(currentGameState.getCapsules())

# Abbreviation
better = betterEvaluationFunction

