import constants

size = constants.grid_size
type = constants.game_type
dx = [0, 1, 0, -1, -1, 1]
dy = [-1, -1, 1, 1, 0, 0]


class play:
    def __init__(self):
        self.board = [[0 for r in range(size)] for c in range(size)]
        self.mode = 1 if type else -1
        self.winner = 0

    def isValid(self, r, c):
        temp = True
        if r < 0 or r > size - 1 or c < 0 or c > size - 1:
            temp = False
        elif self.board[r][c] != self.mode:
            temp = False
        return temp

    def update(self, r, c):
        self.board[r][c] = self.mode
        self.isWon(self.mode)
        self.mode = - self.mode

    def isWon(self, human_mode):
        judger = [[0 for r in range(size)] for c in range(size)]
        temp = True
        if human_mode == -1:
            for j in range(size):
                if self.board[0][j] == -1:
                    judger[0][j] = -2

            while temp:
                flag = False
                for i in range(size):
                    for j in range(size):
                        if judger[i][j] == -2:
                            for k in range(6):
                                if self.isValid(i + dx[k], j + dy[k]) and judger[i + dx[k]][j + dy[k]] == 0:
                                    if i + dx[k] == size - 1:
                                        self.winner = -1
                                        return True
                                    else:
                                        judger[i + dx[k]][j + dy[k]] = -2
                                        temp = True
                            judger[i][j] = -1

        elif human_mode == 1:
            for i in range(size):
                if self.board[i][0] == 1:
                    judger[i][0] = 2

            while temp:
                temp = False
                for i in range(size):
                    for j in range(size):
                        if judger[i][j] == 2:
                            for k in range(6):
                                if self.isValid(i + dx[k], j + dy[k]) and judger[i + dx[k]][j + dy[k]] == 0:
                                    if j + dy[k] == size - 1:
                                        self.winner = 1
                                        return True
                                    else:
                                        judger[i + dx[k]][j + dy[k]] = 2
                                        temp = True
                            judger[i][j] = 1
        return False