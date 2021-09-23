from enum import Enum, auto


class Color(Enum):
    BLACK = auto()
    WHITE = auto()

    @property
    def opponent(self):
        if self == self.BLACK:
            return self.WHITE
        else:
            return self.BLACK


class GameMaster:

    def __init__(self, size=19):
        self.size = size
        self.board = []
        self.next_color = Color.BLACK
        self.moves = []
        row = []
        for i in range(self.size + 2):
            row.append(0)
        for i in range(self.size + 2):
            row = row.copy()
            self.board.append(row)

    def move(self, x, y):

        print(x, y, self.next_color)
        if self.board[y][x] in [1, 2]:
            print("already stone exist")
            # raise ValueError
        self.board[y][x] = self.next_color
        self.moves.append((x, y, self.next_color))
        self.on_end_move()

    def pass_(self):
        self.moves.append((-1, -1, self.next_color))
        self.on_end_move()

    def on_end_move(self):
        self.next_color = self.next_color.opponent

    def print_cui(self):
        chars = [
            ["┌"] + ["┬"] * (self.size - 2) + ["┐"]]
        [chars.append(["├"] + ["┼"] * (self.size - 2) + ["┤"]) for i in range(self.size - 2)]
        chars.append(["└"] + ["┴"] * (self.size - 2) + ["┘"])

        for i, row in enumerate(self.board[1:-1]):
            for j, point in enumerate(row[1:-1]):
                if point == Color.BLACK:
                    chars[j][i] = "●"
                elif point == Color.WHITE:
                    chars[j][i] = "○"

        for char_row in chars:
            row_str = " ".join(char_row)
            print(row_str)


if __name__ == "__main__":
    game_master = GameMaster()
    game_master.move(4, 4, 1)
    print(game_master.board)
    game_master.print_cui()
