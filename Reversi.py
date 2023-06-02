piece_num_ls = []
# choice pvp or robot
def choice_type():
    global robot_level
    check = True
    while check:
        choice = input("1: player vs player    2: player vs robot\n")
        if choice == "1":
            check = False
            robot_level = False
            robot = False
        
        elif choice == "2":
            robot_level = input("1: easy    2:hard\n")
            robot = True
            if robot_level == "1":
                robot_level = "easy"
                check = False
            
            elif robot_level == "2":
                robot_level = "hard"
                check = False
            
            else:
                print("invaild input")
        
        else:
            print("invalid input")
    return robot

# make the table
def make_table(table_ls):
    table_ls = [[' ']*8 for i in range(8)]
    table_ls[3][4] = "●"
    table_ls[4][3] = "●"
    table_ls[3][3] = "○"
    table_ls[4][4] = "○"
    return table_ls

# print the table
def print_table(table_ls):
    line = "    " + "--- " * 8
    print("     A   B   C   D   E   F   G   H")
    
    for x in range(1,9):
        table = ""
        for i in range(8):
            table += f" | {table_ls[x - 1][i]}"
        table += " |"
        print(line)
        print(f"{x} {table}")
    
    print(line)
    print("\n\n\n")

# check the move if it is a valid move
def isvalidmove(y, x, table_ls, hint_ls):
    y_st = y
    x_st = x
    if table_ls[y][x] == "○":
        player = "○"
        next_player = "●"
    else:
        player = "●"
        next_player = "○"
    global piece_num, piece_ls, piece_num_ls
    piece_num = 0
    piece_ls = []
    dir_ls = [[1,0], [0,1], [0,-1], [-1,0], [1,1], [-1,-1], [1,-1], [-1,1]]
    
    for x_dir, y_dir in dir_ls:
        num = 0
        y = y_st
        x = x_st
        x += x_dir
        y += y_dir
        
        if x < 7 and x > 0 and y < 7 and y > 0:
            while table_ls[y][x] == next_player:
                piece_num += 1
                num += 1
                x += x_dir
                y += y_dir
                
                if x > 7 or x < 0 or y > 7 or y < 0:
                    piece_num -= num
                    break
                
                if table_ls[y][x] == " ":
                    piece_num_ls.append(piece_num)
                    piece_num = 0
                    hint_ls.append([y, x])
                
                elif table_ls[y][x] == player:
                    piece_num -= num
                    for i in range(num):
                        x -= x_dir
                        y -= y_dir
                        piece_ls.append([y, x])
                    break
    return table_ls

# change piece
def change_piece_fn(piece_ls, player, table_ls):
    for y, x in piece_ls:
        table_ls[y][x] = player
    return table_ls

# add hint
def add_hint_fn(table_ls, player):
    global piece_num_ls
    hint_ls = []
    piece_num_ls = []
    for i in range(8):
        for k in range(8):
            if table_ls[i][k] == player:
                isvalidmove(i, k, table_ls, hint_ls)
    for y, x in hint_ls:
        table_ls[y][x] = "."
    return hint_ls, table_ls

# del hint
def del_hint_fn(hint_ls, player_move_ls, table_ls):
    for hint in hint_ls:
        if player_move_ls != hint:
            hint_x = hint[0]
            hint_y = hint[1]
            table_ls[hint_x][hint_y] = " "
    
    return table_ls
    
#check if player's move is on the table
def isontable(x, y):
    if x > -1 and x < 9 and type(y) == int:
        return True
    
    else:
        return False

# change player
def change_player(player, next_player):
    if player == "○":
        player = "●"
        next_player = "○"
    
    else:
        player = "○" 
        next_player = "●"   
    
    return player, next_player

# number the letter
letter_number = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
number_letter = {0 : "A", 1 : "B", 2 : "C", 3 : "D", 4 : "E", 5 : "F", 6 : "G", 7 : "H"}

# player's move
def player_turn(player, table_ls, hint_ls):
    letter = ["A","B","C","D","E","F","G","H"]
    check = True
    y = 0
    
    while check:
        player_move_ls = []
        player_move = input(f"{player}'s turn (e.g. A1/b6): ")
        
        for i in player_move.replace(" ",""):
            player_move_ls.append(i)
        
        player_move_ls[0] = player_move_ls[0].upper()
        y = int(player_move_ls[1]) - 1
        player_move_ls[1] = player_move_ls[0]
        player_move_ls[0] = y
        
        if player_move_ls[1] in letter:
            player_move_ls[1] = int(letter_number[player_move_ls[1]])
        if not isontable(player_move_ls[0], player_move_ls[1]) or not player_move_ls in hint_ls:
            print("Error: Invalid location")
        
        else:
            check = False
    
    if player == "○":
        table_ls[player_move_ls[0]][player_move_ls[1]] = "○"
    
    else:
        table_ls[player_move_ls[0]][player_move_ls[1]] = "●"
    
    return player_move_ls

# check win
def check_win(table_ls, hint_ls, game_over):
    game = True
    player1 = 0
    player2 = 0
    
    if hint_ls == []:
        game_over += 1
    
    else:
        game_over = 0

    if game_over == 2:
        for i in table_ls:
            for j in i:
                if j == "●":
                    player1 += 1
                
                else:
                    player2 +=1
            
        if player1 > player2:
            print("player ● win")
            
        else:
            print("player ○ win")
        game = False
    
    return game

# robot move
# easy robot: it will take the position which can eat the most of piece
# hard robot: prioritize the corner position and avoid the player from taking the corner position
def robot_move(piece_num_ls, hint_ls, table_ls):
    avoid_move_ls = [[0, 1], [1, 0], [1, 1], [7, 0], [7, 1], [6, 0], [6, 1], [1, 7], [1, 6], [0, 7], [0, 6],[7, 7], [7, 6], [6, 7], [6, 6]]
    priority_positon = [[0, 0], [7, 7], [0, 7], [7, 0]]
    global robot_move_ls
    robot_move_ls = []
    max = 0
    for i in piece_num_ls:
        if i > max:
            max = i
    if max != 0:
        move_1 = []
        move_2 = []
        move = piece_num_ls.index(max)
        if robot_level == "easy":
            y, x = hint_ls[move]
        elif robot_level == "hard":
            for i in hint_ls:
                if i in priority_positon:
                    move_1 = i
                    break
                elif not i in avoid_move_ls:
                    move_2 = hint_ls[move]
                    break
            if move_1 != []:
                y, x = move_1
            else:
                if move_2 != []:
                    print(move_2)
                    y, x = move_2
                else:
                    y, x = hint_ls[move]
        robot_move_ls.append(y)
        robot_move_ls.append(x)
        table_ls[y][x] = "○"
        x = number_letter[x]
        print(f"robot move: {x} {y + 1}")

# run
def main():
    table_ls = []
    game_over = 0
    game = True
    player = "●"
    next_player = "○"
    player_move_ls = []
    hint_ls = []
    robot = choice_type()
    table_ls = make_table(table_ls)
    hint_ls, table_ls = add_hint_fn(table_ls, player)
    print_table(table_ls)
    table_ls = del_hint_fn(hint_ls, player_move_ls, table_ls)
    
    while game:
        player_move_ls = player_turn(player, table_ls, hint_ls)
        table_ls = isvalidmove(player_move_ls[0], player_move_ls[1], table_ls, hint_ls)
        table_ls = change_piece_fn(piece_ls, player, table_ls)
        player, next_player = change_player(player, next_player)
        hint_ls, table_ls = add_hint_fn(table_ls, player)
        if robot:
            robot_move(piece_num_ls, hint_ls, table_ls)
            table_ls = del_hint_fn(hint_ls, robot_move_ls, table_ls)
            game = check_win(table_ls, hint_ls)
            table_ls = isvalidmove(robot_move_ls[0], robot_move_ls[1], table_ls, hint_ls)
            table_ls = change_piece_fn(piece_ls, player, table_ls)
            player, next_player = change_player(player, next_player)
            hint_ls, table_ls = add_hint_fn(table_ls, player)
        print_table(table_ls)
        table_ls = del_hint_fn(hint_ls, player_move_ls, table_ls)
        game = check_win(table_ls, hint_ls, game_over)

if __name__ == "__main__":
    main()