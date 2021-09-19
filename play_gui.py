from enum import Enum
from enum import  auto

from game_master import GameMaster


class TransfarType(Enum):
    nothing = auto()
    rotate_90 = auto()
    rotate_180 = auto()
    rotate_270 = auto()
    h_flip = auto()
    h_flip_rotate_90 = auto()
    h_flip_rotate_180 = auto()
    h_flip_rotate_270 = auto()


class SgfData:
    def __init__(self, s):
        self.move_count = 0
        self.event_name = "-"
        self.game_datetime = "-"
        self.black_player = "-"
        self.white_player = "-"
        self.komi = 0
        self.moves = []
        self.result = "-"
        self.winner = "-"
        self.board_size = 19
        self.game_name = "-"
        self.place_name = "-"

        self.parse(s)
        self.transfar_type = 0

    def char2idx(self, char):
        idx = "abcdefghij".index(char)

        return idx

    def chars2idx(self, chars):
        return self.char2idx(chars[0]), self.char2idx(chars[1])

    def parse_result(self, result):
        if result == 0:
            self.winner = "-"
            self.result = "持碁"
            return

        winner, result = result.split("+")
        if winner == "B":
            self.winner = "黒"
        elif winner == "W":
            self.winner = "白"
        else:
            raise ValueError

        if result.isdigit():
            self.result = f"{result}目勝ち"
        elif result == "R":
            self.result = "中押し勝ち"
        elif result == "T":
            self.result = "時間切れ"
        else:
            raise ValueError

    def add_value(self, type, value):
        if type == "EV":
            self.event_name = value
        elif type == "DT":
            self.game_datetime = value
        elif type == "PB":
            self.black_player = value
        elif type == "PW":
            self.white_player = value
        elif type == "KM":
            self.komi = float(value)
        elif type == "SZ":
            self.board_size = value + "路盤"
        elif type == "GN":
            self.game_name = value
        elif type == "PC":
            self.place_name = value
        elif type == "RE":
            self.parse_result(value)
        elif type == "B":
            self.moves.append(("B", value))
            self.move_count += 1
        elif type == "W":
            self.moves.append(("W", value))
            self.move_count += 1
        else:
            raise ValueError

    def play(self):
        game_master = GameMaster(9)
        for move in self.moves:
            x, y = self.chars2idx(move[1])
            game_master.move(x, y, 1)
            game_master.print_cui()

    def print(self):
        print("move_count", self.move_count)
        print("event_name", self.event_name)
        print("game_datatime", self.game_datetime)
        print("black_player", self.black_player)
        print("white_player", self.white_player)
        print("komi", self.komi)
        print("winner", self.winner)
        print("result", self.result)
        print("board_size", self.board_size)
        print("game_name", self.game_name)
        print("place_name", self.place_name)
        print("moves", self.moves)

    def parse(self, s):
        moves = s[1:-1].split(";")
        print(moves)
        for move in moves:
            if not move:
                continue
            elements = move.split("]")
            for element in elements:
                if not element:
                    continue
                type, value = element.split("[")

                self.add_value(type, value)

        self.print()


def main():
    with open("k00000114064.sgf") as f:
        s = f.read()
    print(s)

    sgf = SgfData(s)
    sgf.play()


if __name__ == "__main__":
    main()
