"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Nov. 1, 2023
"""

def is_empty(board):
    for i in range (len(board)):
        for j in range (len(board[0])):
            if board[i][j] != " ":
                return False

    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):

    before_open = False
    after_open = False

    #beginning positions
    y_start = y_end - (d_y * (length - 1))
    x_start = x_end - (d_x * (length - 1))

    #Before
    x_before = x_start - d_x
    y_before = y_start - d_y

    if 0 <= x_before < (len(board[0])) and 0 <= y_before < len(board):
        before_open = (board[y_before][x_before] == " ")

    #After
    x_after = x_end + d_x
    y_after = y_end + d_y

    if 0 <= x_after < (len(board[0])) and 0 <= y_after < len(board):
        after_open = (board[y_after][x_after] == " ")

    #Open, Semi-Open or Closed
    if before_open and after_open:
        return "OPEN"
    elif before_open or after_open:
        return "SEMIOPEN"
    else:
        return "CLOSED"


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    #initialize
    open_seq_count, semi_open_seq_count = 0,0

    #renaming values
    x = x_start
    y = y_start
    h = len(board)
    w = len(board[0])

    #Going through the board
    while 0 <= x < w and 0 <= y < h:

        #checking for sequence
        sequence_length = 0
        for i in range (length):
            if 0 <= x + (i * d_x) < w and 0 <= y + (i * d_y) < h and board[y + (i * d_y)][x + (i * d_x)] == col:
                sequence_length += 1
            else:
                break

        #Only count if sequence is required length
        if sequence_length == length:

            #establishing end position

            x_end = x + (d_x * (length - 1))
            y_end = y + (d_y * (length - 1))

            #checking for subparts
            before_valid = not (0 <= x - d_x < w and 0 <= y - d_y < h and board[y - d_y][x - d_x] == col)
            after_valid = not (0 <= x_end + d_x < w and 0 <= y_end + d_y < h and board[y_end + d_y][x_end + d_x] == col)

            #establishing openness of before and after positions
            if before_valid and after_valid:
                before_open = (0 <= (x - d_x) < len(board[0]) and 0 <= (y - d_y) < len(board) and board[y - d_y][x - d_x]  == " ")
                after_open = (0 <= (x_end + d_x) < len(board[0]) and 0 <= (y_end + d_y) < len(board) and board[y_end + d_y][x_end + d_x] == " ")

            #adding to sequence count
                if before_open and after_open:
                    open_seq_count += 1
                elif before_open or after_open:
                    semi_open_seq_count += 1
            x += length * d_x
            y += length * d_y

        #Moving through the board
        x += d_x
        y += d_y

    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    #initialize
    open_seq_count, semi_open_seq_count = 0, 0
    height = len(board)
    width = len(board[0])

    #list of possible directions [dy,dx]
    directions = [[0, 1], [1, 0], [1, 1], [1, -1]]

    #Move through every cell
    for y in range (height):
        for x in range (width):
            for d_y, d_x in directions:
                sequence_L = 0

                #check for sequence
                for i in range (length):
                    new_y = y + (i * d_y)
                    new_x = x + (i * d_x)

                    if 0 <= new_y < height and 0 <= new_x < width and board[new_y][new_x] == col:
                        sequence_L += 1
                    else:
                        sequence_L = 0
                        break

                #Check if sequence length is required length
                if sequence_L == length:
                    end_y = y + (length - 1) * d_y
                    end_x = x + (length - 1) * d_x

                    # Check that this sequence is not part of a longer sequence
                    if not (0 <= x - d_x < width and 0 <= y - d_y < height and board[y - d_y][x - d_x] == col) and \
                       not (0 <= end_x + d_x < width and 0 <= end_y + d_y < height and board[end_y + d_y][end_x + d_x] == col):

                        before_open = (0 <= (x - d_x) < len(board[0]) and 0 <= (y - d_y) < len(board) and board[y - d_y][x - d_x]  == " " )
                        after_open = (0 <= (new_x + d_x) < len(board[0]) and 0 <= (new_y + d_y) < len(board) and board[new_y + d_y][new_x + d_x] == " ")

                        if before_open and after_open:
                            open_seq_count += 1
                        elif before_open or after_open:
                            semi_open_seq_count += 1


    return open_seq_count, semi_open_seq_count

def search_max(board):
    #initialize
    best_score = float ('-inf')
    move_y, move_x = 0,0

    #loop through the board
    for y in range (len(board)):
        for x in range (len(board[0])):

            #if slot is empty, try putting on b and calculating the score
            if board[y][x] == " ":
                board[y][x] = "b"
                curr_score = score(board)

                #reinstating the empty slot
                board[y][x] = " "

                #if the score is better, make it the best score and change the best moves
                if curr_score > best_score:
                    best_score = curr_score
                    move_y, move_x = y, x

    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def win_check(board, y, x, col, length):
    directions = [[0, 1], [1, 0], [1, 1], [1, -1]]
    height = len(board)
    width = len(board[0])

    for d_y, d_x in directions:
        sequence = 0
        for i in range(length):
                new_y = y + (i * d_y)
                new_x = x + (i * d_x)
                if 0 <= new_y < height and 0 <= new_x < width and board[new_y][new_x] == col:
                    sequence += 1
                else:
                    break
        if sequence == length:
            prev_y = y - d_y
            prev_x = x - d_x
            next_y = y + (length * d_y)
            next_x = x + (length * d_x)

            if (0 <= prev_y < height and 0 <= prev_x < width and board[prev_y][prev_x] == col) or \
               (0 <= next_y < height and 0 <= next_x < width and board[next_y][next_x] == col):
                continue
            return True
    return False


def is_win(board):

    col = ["b","w"]

    for colour in col:
        for y in range(len(board)):
            for x in range(len(board[0])):
                if win_check(board, y, x, colour, 5) and colour == "b":
                    return "Black won"
                if win_check(board, y, x, colour, 5) and colour == "w":
                    return "White won"

    if all(spot != " " for row in board for spot in row):
        return "Draw"
    return "Continue Playing"

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty SED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0