import sys
from enum import Enum
from enum import  auto

import db
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
        self.event_name = "-"
        self.game_datetime = "-"
        self.black_player = "-"
        self.white_player = "-"
        self.komi = 0
        self.moves = []
        self.result = "-"
        self.winner = "-"
        self.result = "-"
        self.board_size = 19
        self.game_name = "-"
        self.place_name = "-"
        self.last_color = None
        self.transfar_type = 0
        self.parse(s)

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

    def chars_to_flat_idx(self, value):
        return int(f"{self.char2idx(value[1])}{self.char2idx(value[0])}")

    def flat_idx_to_idx(self, flat_idx):
        return [int(c) for c in str(flat_idx)]

    def add_move(self, type_, value):
        if type_ == self.last_color:
            self.moves.append(-1)
        self.moves.append(self.chars_to_flat_idx(value))

    def add_value(self, type_, value):
        if type_ == "EV":
            self.event_name = value
        elif type_ == "DT":
            self.game_datetime = value
        elif type_ == "PB":
            self.black_player = value
        elif type_ == "PW":
            self.white_player = value
        elif type_ == "KM":
            self.komi = float(value)
        elif type_ == "SZ":
            self.board_size = int(value)
        elif type_ == "GN":
            self.game_name = value
        elif type_ == "PC":
            self.place_name = value
        elif type_ == "RE":
            self.parse_result(value)
        elif type_ in ["B", "W"]:
            self.add_move(type_, value)
        else:
            print('not supported:',type_)

    def play(self):
        game_master = GameMaster(self.board_size)
        for i, move in enumerate(self.moves):
            if move is None:
                game_master.pass_()
                continue
            x, y = self.flat_idx_to_idx(move)
            color = i % 2 + 1
            game_master.move(x, y, color)
            game_master.print_cui()

    def print(self):
        print("event_name", self.event_name)
        print("game_datetime", self.game_datetime)
        print("black_player", self.black_player)
        print("white_player", self.white_player)
        print("komi", self.komi)
        print("winner", self.winner)
        print("result", self.result)
        print("board_size", f"{self.board_size}路盤")
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

    def insert_db(self):
        values={}
        for i,move in enumerate(self.moves):
            values[f"move{i}"] = move

        db.games.insert().execute(**values)
def main():
    with open(sys.argv[1]) as f:
        s = f.read()
    print(s)

    sgf = SgfData(s)
    sgf.play()

if __name__ == "__main__":
    main()
