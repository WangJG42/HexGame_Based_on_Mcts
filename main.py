from play import play
from mcts import mcts
print("输入格式： 3,4")


class gameUnit:
    def __init__(self):
        self.play = play()
        self.isLoop = 1

    def main(self):
        while self.isLoop:
            move = input("请输入r,c:\n")
            if move == 0:
                break
            else:
                location = list(map(eval, move.split(',', 2)))
                a, b = location[0], location[1]
                self.play.update(a, b)
                if self.play.winner != 0:
                    winner_label = ""
                    if self.play.winner == -1:
                        winner_label = " -1 ( Blue ) "
                    else:
                        winner_label += " 1 ( Red ) "
                    print(winner_label)

                else:
                    AI = mcts(a, b, -self.play.mode, self.play.board)
                    e = AI.move()
                    self.play.update(e[0], e[1])
                    if self.play.winner != 0:
                        if self.play.winner == -1:
                            print('-1赢了')
                        else:
                            print(" 1赢了 ")
game = gameUnit()
game.main()