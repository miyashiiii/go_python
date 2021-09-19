class GameMaster:
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    FRAME = 3

    def __init__(self, size=19):
        self.size = size
        self.board=[]
        row=[]
        for i in range(self.size+2):
            row.append(0)
        for i in range(self.size+2):
            row = row.copy()
            self.board.append(row)

    def move(self, x, y, color):
        if self.board[y+1][x+1]in [1,2]:
            print("already stone exist")
            # raise ValueError
        self.board[y + 1][x + 1] = color
    def pass_(self):
        pass
    def print_cui(self):
        chars = [
            ["┌", "┬", "┬", "┬", "┬", "┬", "┬", "┬", "┐"],
            ["├", "┼", "┼", "┼", "┼", "┼", "┼", "┼", "┤"],
            ["├", "┼", "┼", "┼", "┼", "┼", "┼", "┼", "┤"],
            ["├", "┼", "┼", "┼", "┼", "┼", "┼", "┼", "┤"],
            ["├", "┼", "┼", "┼", "┼", "┼", "┼", "┼", "┤"],
            ["├", "┼", "┼", "┼", "┼", "┼", "┼", "┼", "┤"],
            ["├", "┼", "┼", "┼", "┼", "┼", "┼", "┼", "┤"],
            ["├", "┼", "┼", "┼", "┼", "┼", "┼", "┼", "┤"],
            ["└", "┴", "┴", "┴", "┴", "┴", "┴", "┴", "┘"],
        ]
        for i, row in enumerate(self.board[1:-1]):
            for j, point in enumerate(row[1:-1]):
                if point == self.BLACK:
                    chars[j][i] = "●"
                elif point == self.WHITE:
                    chars[j][i] = "○"

        for char_row in chars:
            row_str = " ".join(char_row)
            print(row_str)

if __name__ == "__main__":
    game_master = GameMaster()
    game_master.move(4,4,1)
    print(game_master.board)
    game_master.print_cui()
