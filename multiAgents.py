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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        ghStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        mini = float('inf')
        
        for i in newFood:
            mini = min(mini,manhattanDistance(i,newPos))

        return successorGameState.getScore() + 1.0/mini



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

        depth = 0

        return self.getMaxValue(gameState, depth)[1]

    def getMaxValue(self, gState, depth, a = 0):
        actions = gState.getLegalActions(a)

        if not actions or gState.isWin() or depth >= self.depth:
            return self.evaluationFunction(gState), Directions.STOP

        sucCost = float('-inf')
        sucAction = Directions.STOP

        for act in actions:
            suc = gState.generateSuccessor(a, act)

            cost = self.getMinValue(suc, depth, a + 1)[0]

            if cost > sucCost:
                sucCost = cost
                sucAction = act

        return sucCost, sucAction

    def getMinValue(self, gState, depth, a):
        actions = gState.getLegalActions(a)

        if not actions or gState.isLose() or depth >= self.depth:
            return self.evaluationFunction(gState), Directions.STOP

        sucCost = float('inf')
        sucAction = Directions.STOP

        for act in actions:
            suc = gState.generateSuccessor(a, act)

            cost = 0

            if a == gState.getNumAgents() - 1:
                cost = self.getMaxValue(suc, depth + 1)[0]
            else:
                cost = self.getMinValue(suc, depth, a + 1)[0]

            if cost < sucCost:
                sucCost = cost
                sucAction = act

        return sucCost, sucAction


        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        alpha = float('-inf')
        beta = float('inf')
        return self.getMaxValue(gameState, alpha, beta, depth)[1]

    def getMaxValue(self, gState, alpha, beta, depth, a = 0):
        actions = gState.getLegalActions(a)

        if not actions or gState.isWin() or depth >= self.depth:
            return self.evaluationFunction(gState), Directions.STOP

        sucCost = float('-inf')
        sucAction = Directions.STOP

        for act in actions:
            suc = gState.generateSuccessor(a, act)

            cost = self.getMinValue(suc, alpha, beta, depth, a + 1)[0]

            if cost > sucCost:
                sucCost = cost
                sucAction = act

            if sucCost > beta:
                return sucCost, sucAction

            alpha = max(alpha, sucCost)

        return sucCost, sucAction

    def getMinValue(self, gState, alpha, beta, depth, a):
        actions = gState.getLegalActions(a)

        if not actions or gState.isLose() or depth >= self.depth:
            return self.evaluationFunction(gState), Directions.STOP

        sucCost = float('inf')
        sucAction = Directions.STOP

        for act in actions:
            suc = gState.generateSuccessor(a, act)

            cost = 0

            if a == gState.getNumAgents() - 1:
                cost = self.getMaxValue(suc, alpha, beta, depth + 1)[0]
            else:
                cost = self.getMinValue(suc, alpha, beta, depth, a + 1)[0]

            if cost < sucCost:
                sucCost = cost
                sucAction = act

            if sucCost < alpha:
                return sucCost, sucAction

            beta = min(beta, sucCost)

        return sucCost, sucAction

        util.raiseNotDefined()

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
        depth = 0
        return self.getMaxValue(gameState, depth)[1]

    def getMaxValue(self, gState, depth, a = 0):
        actions = gState.getLegalActions(a)

        if not actions or gState.isWin() or depth >= self.depth:
            return self.evaluationFunction(gState), Directions.STOP

        sucCost = float('-inf')
        sucAction = Directions.STOP

        for act in actions:
            suc = gState.generateSuccessor(a, act)

            cost = self.getMinValue(suc, depth, a + 1)[0]

            if cost > sucCost:
                sucCost = cost
                sucAction = act

        return sucCost, sucAction

    def getMinValue(self, gState, depth, a):
        actions = gState.getLegalActions(a)

        if not actions or gState.isLose() or depth >= self.depth:
            return self.evaluationFunction(gState), None

        sucCosts = []

        for act in actions:
            suc = gState.generateSuccessor(a, act)

            cost = 0

            if a == gState.getNumAgents() - 1:
                cost = self.getMaxValue(suc, depth + 1)[0]
            else:
                cost = self.getMinValue(suc, depth, a + 1)[0]

            sucCosts.append(cost)

        return sum(sucCosts) / float(len(sucCosts)), None
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: This eval-function uses (manhattan) distance between ghosts and pacman, the (manhattan)distance between pacman and capsules, and the current game score.
                 The distance between ghost and pacman is deducted from current score and distance
                 between capsules and pacman is added to current score.
    """
    "*** YOUR CODE HERE ***"

    cap = currentGameState.getCapsules()

    cur_score = currentGameState.getScore()
    gh_score = 0
    c_score = 0

    pcm_pos = currentGameState.getPacmanPosition()
    ghStates = currentGameState.getGhostStates()
    #nFL = currentGameState.getFood().asList()



    if(len(cap) != 0):
        for c in cap:
            c_dis = min([manhattanDistance(c, pcm_pos)])
            if c_dis == 0 :
                c_score = float(1)/c_dis
            else:
                c_score = -100

    for gh in ghStates:
        gh_x = (gh.getPosition()[0])
        gh_y = (gh.getPosition()[1])
        gh_pos = gh_x,gh_y
        gh_dis = manhattanDistance(pcm_pos, gh_pos)

    return cur_score  - (1.0/1+gh_dis)  + (1.0/1+c_score)


# Abbreviation
better = betterEvaluationFunction
