from game_master import GameMaster

board_size = 5
game_master = GameMaster(board_size)
while True:
    point = input("[x, y]:")
    try:
        x, y = point.split(",")
        x = int(x)
        y = int(y)
        if not 1 <= x <= board_size or not 1 <= y <= board_size:
            ValueError()
    except Exception:
        print("invalid input")
        continue
    game_master.move(x, y)
    game_master.print_cui()
