from game_master import GameMaster

board_size = 5
game_master = GameMaster(board_size)
while True:
    print("next:",game_master.current_color)
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
    try:
        game_master.move(x, y)
    except ValueError as e:
        print(e)
    game_master.print_cui()

