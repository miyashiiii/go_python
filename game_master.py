from enum import Enum, auto


class Color(Enum):
    black = auto()
    white = auto()

    @property
    def opponent(self):
        if self == self.black:
            return self.white
        else:
            return self.black

    def to_square(self):
        if self == self.black:
            return Square.black
        else:
            return Square.white

    def __str__(self):
        return self.name


class Square(Enum):
    empty = auto
    black = auto()
    white = auto()

    @staticmethod
    def from_color(color):
        if color == Color.black:
            return Square.black
        if color == Color.white:
            return Square.white
        raise ValueError("")


class GameMaster:

    def __init__(self, size=19):
        self.size = size
        self.board = []
        self.current_color = Color.black
        self.moves = []
        row = []
        for i in range(self.size):
            row.append(Square.empty)
        for i in range(self.size):
            row = row.copy()
            self.board.append(row)
        self.refresh_checked_board()
        self.recursive = 0

        self.black_hama = 0
        self.white_hama = 0
        self.last_hama_num = 0

    def refresh_checked_board(self):
        self.checked_board = []
        row = []
        for i in range(self.size):
            row.append(False)
        for i in range(self.size):
            row = row.copy()
            self.checked_board.append(row)

    def check_suicide(self, x, y):
        self.checked_board[y][x] = True
        self.current_color = self.current_color.opponent
        captured = self.check_captured_recursive(x, y)
        self.refresh_checked_board()
        self.current_color = self.current_color.opponent
        if captured is not None:
            return True
        else:
            return False

    def move(self, x, y):
        print("input: ", x, y, self.current_color)
        try:
            square = self.board[y][x]
        except IndexError:
            raise ValueError("invalid index")
        if square in [Square.black, Square.white]:
            raise ValueError("already stone exist.")
            # raise ValueError
        self.board[y][x] = self.current_color.to_square()
        self.remove_captured_stone(x, y)
        is_suicide = self.check_suicide(x, y)
        if is_suicide:
            self.board[y][x] = Square.empty
            raise ValueError("it is suicide")

        self.moves.append((x, y, self.current_color))
        self.on_end_move()

    def pass_(self):
        self.moves.append((-1, -1, self.current_color))
        self.on_end_move()

    def on_end_move(self):
        self.current_color = self.current_color.opponent

    def print_cui(self):
        chars = [
            ["???"] + ["???"] * (self.size - 2) + ["???"]]
        [chars.append(["???"] + ["???"] * (self.size - 2) + ["???"]) for i in range(self.size - 2)]
        chars.append(["???"] + ["???"] * (self.size - 2) + ["???"])

        for i in range(self.size):
            for j in range(self.size):
                square = self.board[j][i]
                if square == Square.black:
                    chars[j][i] = "???"
                elif square == Square.white:
                    chars[j][i] = "???"

        for char_row in chars:
            row_str = " ".join(char_row)
            print(row_str)

    DIRECTIONS = (
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
    )

    def remove_captured_stone(self, x, y):
        captured_squares = []
        for dx, dy in self.DIRECTIONS:
            self.recursive = 0
            check_x = x + dx
            check_y = y + dy

            # print(f"check [{check_x}, {check_y}]")
            try:
                if self.checked_board[check_y][check_x]:
                    continue
                if not 0 <= check_x <= self.size or not 0 <= check_y <= self.size:
                    continue
                square = self.board[check_y][check_x]
                self.checked_board[check_y][check_x] = True
                if square == self.current_color.opponent.to_square():
                    captured = self.check_captured_recursive(check_x, check_y)
                    if captured is not None:
                        captured_squares += captured

            except IndexError:
                continue

        print("cap list:", captured_squares)
        if captured_squares is not None:
            # ??????????????????
            if len(captured_squares) == 1 and self.last_hama_num == 1 \
                    and self.moves[-1][0] == captured_squares[0][0] \
                    and self.moves[-1][1] == captured_squares[0][1]:
                self.board[y][x] = Square.empty
                raise ValueError("ko")

            for x, y in captured_squares:
                self.board[y][x] = Square.empty
            self.last_hama_num = len(captured_squares)
            if self.current_color == Color.black:
                self.black_hama += self.last_hama_num
            else:
                self.white_hama += self.last_hama_num
        else:
            self.last_hama_num = 0
        self.refresh_checked_board()

    def check_captured_recursive(self, x, y):
        self.recursive += 1

        print(self.recursive)
        # return list or None
        captured = []
        for dx, dy in self.DIRECTIONS:
            nextx = x + dx
            nexty = y + dy
            """
            capture???????????????: continue
            capture???????????????: return None
            
            """
            try:

                # ????????????continue (capture???????????????)
                if nextx < 0 or nextx > self.size or nexty < 0 or nexty > self.size:
                    continue
                # check????????????continue (capture???????????????)
                if self.checked_board[nexty][nextx]:
                    continue
                # print("next:",nextx,nexty)
                square = self.board[nexty][nextx]
                self.checked_board[nexty][nextx] = True

                # ????????????continue (capture???????????????)
                if square == self.current_color.to_square():
                    continue
                # ?????????????????????????????????????????? (capture???????????????)
                elif square == self.current_color.opponent.to_square():
                    captured_tmp = self.check_captured_recursive(nextx, nexty)
                    if captured_tmp is None:
                        return None
                    else:
                        self.checked_board[nexty][nextx] = True

                        captured += captured_tmp
                elif square == Square.empty:
                    # print("empty")
                    return None

            except IndexError:
                # ??????
                continue

        return captured + [[x, y]]


if __name__ == "__main__":
    game_master = GameMaster(5)
    try:
        game_master.move(1, 0)
        game_master.move(0, 0)
        game_master.move(0, 1)
        game_master.print_cui()
        game_master.move(0, 0)
        game_master.print_cui()
    except ValueError as e:
        print("ERROR:", e)
