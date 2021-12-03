
"""
config variables
"""
valid_sizes = ['3x3', '4x4', '5x5']

"""
pleas no touchy 
"""
game_on = False
turn_counter = 1
program_on = True
rows = False
columns = False
diags = False
tie = False


def init_variables():
    global game_on
    game_on = False
    global turn_counter
    turn_counter = 1
    global program_on
    program_on = True
    global rows
    rows = False
    global columns
    columns = False
    global diags
    diags = False
    global tie
    tie = False
    return


def board_size(valid_size):
    """
    prompt user to enter a valid board size to play
    """

    size_ask = ''

    while str(size_ask) not in valid_size:
        size_ask = input(f"Please enter which size board you'd like to play on ({','.join(valid_size)}): ")
    else:
        print("3x3 selected!")
    size_ask.split('x')
    game = True
    return size_ask, game


def create_board(size_ask):
    """
    create a list of lists with all spaces and fills with a '0'
    """

    board_spaces = [[' ' for x in range(0, int(size_ask[2]))] for y in range(0, int(size_ask[0]))]
    return board_spaces


def display_board(board_spaces):
    """
    print current board
    """

    for iteration, row in enumerate(board_spaces):
        row = ' | '.join(row)
        if iteration in range(1, len(board_spaces)):
            raw_barrier = ('-' * 3 + '|') * len(board_spaces)
            format_barrier = raw_barrier.rstrip(raw_barrier[-1])
            print(format_barrier)
        print(' ' + row)


def move_input(board_spaces, turn):
    """
    takes raw input from prompt, checks if it's a valid input, and returns x, y coordinates as ints
    """

    column = -1
    row = -1
    valid_check = False
    column_amount = len(board_spaces[0])
    row_amount = len(board_spaces)

    while int(column) not in range(1, column_amount + 1):
        column = input(f'Player {turn}, Please enter a valid column: ')
        try:
            int(column)
        except ValueError:
            column = -1

    while int(row) not in range(1, row_amount + 1):
        row = input(f'Player {turn}, Please enter a valid row: ')
        try:
            int(row)
        except ValueError:
            row = -1

    if board_spaces[int(row) - 1][int(column) - 1] in ['X', 'O']:
        print("Please enter a valid, empty coordinate.")
        column = -1
        row = -1
    else:
        valid_check = True

    return int(column), int(row)


def update_board(column, row, board_spaces, turn):
    """
    update board list of lists with turn based player coordinates
    """

    if turn == 1:
        piece = 'X'
    elif turn == 2:
        piece = 'O'

    board_spaces[row - 1][column - 1] = piece

    return board_spaces


def change_turn(turn):
    """
    changes turn
    """
    if turn == 1:
        turn = 2
    elif turn == 2:
        turn = 1
    return turn


def check_rows(board):
    """
    checks all rows for win condition
    """
    for x in board:
        if len(set(x)) == 1 and len(x) == len(board[0]) and x[0] in ['X', 'O']:
            return True
        else:
            pass
    return False


def check_columns(board):
    """
    checks all columns for win condition
    """
    col_check = [[x[n] for x in board] for n, y in enumerate(board)]
    for x in col_check:
        if len(set(x)) == 1 and len(x) == len(board[0]) and x[0] in ['X', 'O']:
            return True
        else:
            pass
    return False


def check_diags(board):
    # yes i know DRY but i dunno how else to do it cool-y
    """
    check all diagonals for win condition
    """
    pos = [x[i] for i, x in enumerate(board)]
    neg = [x[i] for i, x in enumerate(board[::-1])]

    for x in [pos, neg]:
        if len(set(x)) == 1 and len(x) == len(board[0]) and x[0] in ['X', 'O']:
            return True
        else:
            pass
    return False


def check_win(rows_check, column_check, diag_check):
    """
    check if a win condition is met, if not update turn count and continue, else break main game loop to win,
    if won, returns FALSE to turn off game_on
    """

    if any([rows_check, column_check, diag_check]):
        return False
    else:
        return True


def print_win(turn):
    """
    print out win screen
    """
    win_turn = change_turn(turn)
    print(f'Wow!! Player {win_turn} won')


def play_again():
    """
    prompt user to play again
    """
    play = ''
    while play.lower() not in ['y', 'yes', 'n', 'no']:
        play = input('Play again? Y or N: ')
    if play.lower() in ['y', 'yes']:
        return True
    else:
        return False


"""
main loop
"""

while program_on:
    # resets all global variables
    init_variables()

    # prompt board size and update game state
    size, game_on = board_size(valid_sizes)

    # create list containing all board spaces
    playing_board = create_board(size)

    while game_on:
        # display board
        display_board(playing_board)

        # prompt move and return x and y values of input as int
        column_input, row_input = move_input(playing_board, turn_counter)

        # update board and return updated board,
        playing_board = update_board(column_input, row_input, playing_board, turn_counter)

        # check rows
        rows, columns, diags = check_rows(playing_board), check_columns(playing_board), check_diags(playing_board)

        # check if win state is reached
        game_on = check_win(rows, columns, diags)

        # switches turn counter
        turn_counter = change_turn(turn_counter)


        # tie check
        if ' ' not in [item for sublist in playing_board for item in sublist] and game_on:
            tie = True
            game_on = False
        else:
            pass

    if not tie:
        # displays winning board
        display_board(playing_board)

        # displays winner
        print_win(turn_counter)

        # prompt user to play again, or close program
        program_on = play_again()
    else:
        # tie screen
        display_board(playing_board)
        print('Wow! You Tied!')
        program_on = play_again()
