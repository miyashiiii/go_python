from game_master import GameMaster

board_size = 5
game_master = GameMaster(board_size)

game_master.move(0, 0)
game_master.move(1, 0)
game_master.move(1, 1)
game_master.move(0, 1)
game_master.move(0, 2)
game_master.pass_()
game_master.move(0, 0)

game_master.print_cui()

while True:
    print("next:", game_master.current_color)
    point = input("[x, y]:")
    if point in ["pass", "p"]:
        game_master.pass_()
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
        print("ERROR: ",e)
    game_master.print_cui()
    print("black hama:", game_master.black_hama)
    print("white hama:", game_master.white_hama)
