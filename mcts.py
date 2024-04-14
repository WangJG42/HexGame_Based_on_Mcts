import constants
import math
import random

size = constants.grid_size
type = constants.game_type
dx = [0, 1, 0, -1, -1, 1]
dy = [-1, -1, 1, 1, 0, 0]


class node:
    def __init__(self, r, c, mctsMode, parent=None):
        self.board = [[0 for r in range(size)] for c in range(size)]
        self.board[r][c] = mctsMode
        self.reward = 0
        self.visit = 0
        self.mode = mctsMode
        self.parent = parent
        self.children = []
        self.location = [r, c]
        if self.parent != None:
            for i in range(size):
                for j in range(size):
                    self.board[i][j] = parent.board[i][j]

    def isValid(self, r, c, board):
        temp = True
        if r < 0 or r > size - 1 or c < 0 or c > size - 1:
            temp = False
        elif board[r][c] != self.mode:
            temp = False
        return temp

    def isWon(self, mcts_mode, board):
        judger = [[0 for r in range(size)] for c in range(size)]
        temp = True
        if mcts_mode == -1:
            for j in range(size):
                if self.board[0][j] == -1:
                    judger[0][j] = -2

            while temp:
                flag = False
                for i in range(size):
                    for j in range(size):
                        if judger[i][j] == -2:
                            for k in range(6):
                                if self.isValid(i + dx[k], j + dy[k], board) and judger[i + dx[k]][j + dy[k]] == 0:
                                    if i + dx[k] == size - 1:
                                        self.winner = -1
                                        return -1
                                    else:
                                        judger[i + dx[k]][j + dy[k]] = -2
                                        temp = True
                            judger[i][j] = -1

        elif mcts_mode == 1:
            for i in range(size):
                if self.board[i][0] == 1:
                    judger[i][0] = 2

            while temp:
                temp = False
                for i in range(size):
                    for j in range(size):
                        if judger[i][j] == 2:
                            for k in range(6):
                                if self.isValid(i + dx[k], j + dy[k], board) and judger[i + dx[k]][j + dy[k]] == 0:
                                    if j + dy[k] == size - 1:
                                        self.winner = 1
                                        return 1
                                    else:
                                        judger[i + dx[k]][j + dy[k]] = 2
                                        temp = True
                            judger[i][j] = 1
        return 0

    def isLeaf(self):
        legal = []
        for i in range(size):
            for j in range(size):
                if self.board[i][j] == 0:
                    legal.append([i, j])
        return True if len(legal)!=0 else False

    def select(self): # mcts 选择节点
        if not len(self.children):
            return self
        best_child, best_uct = self.children[0], -1
        for i in self.children:
            if not i.isleaf():
                uct = i.reward/i.visit + 2*math.sqrt(math.log(self.visit)/i.visit)
                if uct>best_uct:
                    best_uct = uct
                    best_child = i
        return best_child.select()

    def expand(self):
        legal=[]
        for i in range(size):
            for j in range(size):
                if self.board[i][j] == 0:
                    legal.append([i, j])
        for i in self.children:
            legal.remove(i.move)
        if len(legal)==0:
            self.simulate()
        for i in legal:
            child = node(i[0], i[1], -self.mode, self)
            self.children.append(child)
            child.simulate()

    def simulate(self, breadth=constants.breadth):
        value = 0
        for i in range(breadth):
            mode2 = -self.mode
            board2 = [[0 for r in range(size)] for c in range(size)]
            for j in range(size):
                for k in range(size):
                    board2[j][k] = self.board[j][k]
            while True:
                legal = []
                for a in range(size):
                    for b in range(size):
                        if self.board[a][b] == 0:
                            legal.append([a, b])
                if len(legal)==0:
                    break
                rad = random.randint(0, len(legal))
                board2[legal[rad][0]][legal[rad][1]] = mode2
                mode2 = -mode2
            value += self.isWon(self.mode, board2)
        self.reward += value/breadth
        self.visit += 1
        self.backup(value/breadth)

    def backup(self, reward):
        if self.parent == None:
            return
        self.parent.visits += 1
        self.parent.reward += reward
        self.parent.backup(reward)


class mcts:
    def __init__(self,r , c, mode, board):
        self.root = node(r, c, mode, None)
        for i in range(size):
            for j in range(size):
                self.root.board = board[i][j]

    def move(self):
        for iterations in range(constants.iterations):
            self.root.select().expand()

            if iterations % 10!=0:
                continue
            best_location, most_visit, best_reward = [0, 0], 0, 0
            for i in self.root.children:
                if i.visit > most_visit:
                    best_location = i.location
                    most_visit = i.visit
                    best_reward = i.reward
            return best_location



